#!/usr/bin/env python3
"""Validate a static Cloudflare Pages output directory without dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


MAX_FILE_BYTES = 25 * 1024 * 1024
MAX_FREE_PLAN_FILES = 20_000
ASSET_SUFFIXES = {
    ".avif", ".css", ".eot", ".gif", ".ico", ".jpeg", ".jpg", ".js",
    ".json", ".m4v", ".mov", ".mp3", ".mp4", ".ogg", ".otf", ".pdf",
    ".png", ".svg", ".ttf", ".webm", ".webp", ".woff", ".woff2",
}
ATTR_RE = re.compile(r"(?:src|href|poster)\s*=\s*([\"'])(.*?)\1", re.I | re.S)
SRCSET_RE = re.compile(r"srcset\s*=\s*([\"'])(.*?)\1", re.I | re.S)
CSS_URL_RE = re.compile(r"url\(\s*(?:\"([^\"]*)\"|'([^']*)'|([^)]*))\s*\)", re.I)
STATIC_LITERAL_RE = re.compile(r"[\"'](/static/[^\"']+)[\"']", re.I)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def is_local_asset(value: str) -> bool:
    value = value.strip()
    if not value or value.startswith(("#", "data:", "mailto:", "tel:", "javascript:")):
        return False
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return False
    path = unquote(parsed.path)
    return path.startswith(("/static/", "static/", "./static/", "../static/")) or Path(path).suffix.lower() in ASSET_SUFFIXES


def exact_path_status(root: Path, target: Path) -> str | None:
    try:
        relative = target.resolve().relative_to(root.resolve())
    except ValueError:
        return "escapes the publish directory"

    current = root.resolve()
    for part in relative.parts:
        if not current.is_dir():
            return "is missing"
        names = {entry.name for entry in current.iterdir()}
        if part not in names:
            if any(name.casefold() == part.casefold() for name in names):
                return "has different letter case on disk"
            return "is missing"
        current /= part
    if not current.is_file():
        return "is missing"
    return None


def target_for(root: Path, document: Path, value: str) -> Path:
    path = unquote(urlsplit(value.strip()).path)
    if path.startswith("/"):
        return root / path.lstrip("/")
    return document.parent / path


def references(text: str):
    seen: set[tuple[int, str]] = set()
    for regex in (ATTR_RE, CSS_URL_RE, STATIC_LITERAL_RE):
        for match in regex.finditer(text):
            groups = [group for group in match.groups()[1:] if group is not None] if regex is ATTR_RE else [group for group in match.groups() if group is not None]
            if not groups:
                continue
            value = groups[0].strip()
            key = (match.start(), value)
            if key not in seen:
                seen.add(key)
                yield match.start(), value
    for match in SRCSET_RE.finditer(text):
        for item in match.group(2).split(","):
            value = item.strip().split()[0] if item.strip() else ""
            key = (match.start(), value)
            if value and key not in seen:
                seen.add(key)
                yield match.start(), value


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    if not root.is_dir():
        return [f"publish directory does not exist: {root}"]

    files = [path for path in root.rglob("*") if path.is_file()]
    if len(files) > MAX_FREE_PLAN_FILES:
        errors.append(f"site has {len(files)} files; Cloudflare Pages Free supports {MAX_FREE_PLAN_FILES}")
    for path in files:
        if path.stat().st_size > MAX_FILE_BYTES:
            errors.append(f"{path.relative_to(root)} exceeds 25 MiB")

    for required in ("index.html", "404.html", "_redirects"):
        if not (root / required).is_file():
            errors.append(f"required publish file is missing: {required}")

    for document in root.rglob("*.html"):
        text = document.read_text(encoding="utf-8")
        if any(marker in text for marker in ("{{", "{%", "{#")):
            errors.append(f"{document.relative_to(root)} contains Jinja syntax")
        for offset, value in references(text):
            if not is_local_asset(value):
                continue
            status = exact_path_status(root, target_for(root, document, value))
            if status:
                errors.append(
                    f"{document.relative_to(root)}:{line_number(text, offset)} references {value!r}, which {status}"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site_root", nargs="?", default="public", type=Path)
    args = parser.parse_args()
    root = args.site_root.resolve()
    errors = validate(root)
    if errors:
        print(f"FAIL: {len(errors)} problem(s) found in {root}")
        for error in errors:
            print(f"- {error}")
        return 1

    files = [path for path in root.rglob("*") if path.is_file()]
    html_files = list(root.rglob("*.html"))
    largest = max(files, key=lambda path: path.stat().st_size)
    print(f"OK: {len(html_files)} HTML files and {len(files)} total files validated")
    print(f"Largest file: {largest.relative_to(root)} ({largest.stat().st_size / 1024 / 1024:.2f} MiB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

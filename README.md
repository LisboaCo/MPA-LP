# Landing pages — Cloudflare Pages

Este repositório é um site estático. Flask, Gunicorn, Docker e VPS não fazem mais parte da execução.

## Estrutura

- `public/*.html`: landing pages publicadas com URL sem `.html`.
- `public/static/`: imagens, fontes, vídeos e JavaScript compartilhados.
- `public/_redirects`: compatibilidade com as URLs antigas `/lp/<slug>`.
- `public/_headers`: cabeçalhos de segurança enviados pelo Cloudflare Pages.
- `wrangler.jsonc`: configuração para desenvolvimento e deploy pela CLI.

Arquivos que ficam fora de `public/` não são publicados.

## Publicar pelo painel do Cloudflare

1. Crie um projeto em **Workers & Pages > Pages > Import an existing Git repository**.
2. Selecione a branch `main`.
3. Não selecione framework.
4. Deixe o comando de build vazio.
5. Informe `public` como diretório de saída.
6. Depois do primeiro deploy, associe o domínio em **Custom domains**.

## Testar e publicar pela CLI

```powershell
npx wrangler pages dev public
npx wrangler pages deploy public --project-name lp-mpa-advogados
```

## Rotas

- `/` → `public/index.html`
- `/<slug>` → `public/<slug>.html`
- `/lp/<slug>` → redirecionamento permanente para `/<slug>`
- `/lp/help` → inventário JSON das páginas

## Regra para assets

Use caminhos iniciados por `/static/`, mantenha exatamente as mesmas letras maiúsculas e minúsculas do nome do arquivo e aplique URL encoding a espaços (`%20`). O deploy falha na validação se um asset estiver ausente, tiver capitalização incompatível ou exceder 25 MiB.

Valide antes de publicar:

```powershell
python scripts/validate_cloudflare_site.py public
```

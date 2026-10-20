# Padrão de landing pages no Cloudflare Pages

Crie cada nova LP como um HTML completo em `public/<slug>.html`. Não adicione Flask, servidor Python, Docker ou etapa de build.

## Regras obrigatórias

- Salve imagens, fontes, vídeos e JavaScript compartilhado em `public/static/`.
- Referencie assets por `/static/...`, com capitalização idêntica ao arquivo e espaços codificados como `%20`.
- Use um único `h1`, título, description, canonical e metadados Open Graph coerentes.
- Preserve `public/static/tracking.js`, GTM, UTMs e eventos de CTA existentes.
- Mantenha formulários e webhooks no navegador somente quando não houver segredo no código.
- Não coloque tokens, senhas ou chaves privadas em `public/`.
- Mantenha cada arquivo abaixo de 25 MiB.
- Atualize `public/help.json` ao adicionar ou remover uma LP.
- Rode `python scripts/validate_cloudflare_site.py public` antes do deploy.

As URLs canônicas são `/<slug>`. A compatibilidade com `/lp/<slug>` é mantida por `public/_redirects`.

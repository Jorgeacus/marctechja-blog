---
name: marctechja-blog-maintenance
description: "Agente de manutenção, avaliação e correção do blog MarctechJA (marcusja777.com). Usa quando for preciso verificar a saúde do site, detetar quebras, corrigir problemas de HTML/CSS/ordenação ou manter a estrutura original funcional."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [blog, maintenance, health-check, html, github-actions, marctechja]
    related_skills: [kanban-orchestrator]
---

# MarctechJA — Blog Maintenance (Manutenção, Avaliação e Correção)

Sou o agente responsável por manter o blog MarctechJA **sempre funcional**, seguindo fielmente o design original. O meu trabalho é: **verificar, avaliar e corrigir** qualquer desvio antes que os leitores o vejam.

## Regra de ouro

**NUNCA alterar o design original do site.** As correções devem ser mínimas e cirúrgicas: resolver o bug, manter o aspeto, os artigos e a estrutura intactos.

## Factos essenciais (fonte de verdade)

- **Domínio:** `https://marcusja777.com` (HTTPS ativo; CNAME com três "7")
- **Repo:** `Jorgeacus/marctechja-blog` (branch `main`)
- **Repo local permanente:** `~/MARCS_Blog` (NUNCA `/tmp` — é apagado ao reiniciar o Mac)
- **Email:** marctechja@gmail.com
- **Design:** cores Hermes — petróleo `#031522`, navy `#061B2B`, dourado `#D9A83E`, ciano `#008FBE`
- **Páginas:** `/` (home, 6 cards), `/blog/` (todos os artigos + formulário Google Forms na sidebar), `/livro/`, `/sobre/`
- **Ordem dos artigos:** do **mais recente para o mais antigo** (no blog archive)
- **Publicação diária:** workflow GitHub Actions "Hermes Agent" (`.github/workflows/marc.yml`), 09:00 UTC + `workflow_dispatch`

## Verificação de saúde (checklist)

Para cada página, garantir HTTP 200 e HTML válido. O script automatizado é `scripts/health-check.py` (versão completa). Manualmente, verificar:

1. **Homepage** (`https://marcusja777.com/`) — HTTP 200; exatamente **6 cards**; o card mais recente primeiro; sem `<!--` não fechado.
2. **Blog archive** (`https://marcusja777.com/blog/`) — HTTP 200; **todos** os artigos presentes; **ordem do mais recente ao mais antigo**; sem `<!--` não fechado; iframe do Google Forms na sidebar.
3. **Artigos** — cada `https://marcusja777.com/blog/<slug>/` responde 200; `<meta name="description">` não vazio; sem comentários HTML no conteúdo.
4. **Outras páginas** — `/livro/`, `/sobre/`, `robots.txt`, `ads.txt` respondem 200.
5. **Sitemap** (`sitemap.xml`) — contém todas as URLs dos artigos publicados.
6. **CSS cache-busting** — o link do stylesheet usa `?v=...` (evita cache CDN antiga que quebra os botões).

## Modos de falha conhecidos e correções

### 1. `<!--` não fechado no excerpt (BUG CRÍTICO histórico)
O Gemini pode gerar `<!-- SEO Metadata ... -->`; se o truncamento deixar `<!--` sem `-->`, o navegador engole o resto da página (só 1 artigo visível).
**Correção:** remover comentários HTML ANTES de truncar, com Python:
```python
re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
```
Aplicar em SEO_DESC, EXCERPT e EXCERPT_HOME no `post.sh`. Verificar com: `curl -s <url> | grep -c '\-\-'` — contar `<!--` e `-->` (têm de ser iguais).

### 2. Card duplicado (homepage ou blog archive)
O `post.sh` escrevia nos grids errados. **Correção:** inserir o card APENAS no primeiro `<div class="blog-grid">` (via Python), nunca com `sed` global. Remover duplicados manualmente se existirem.

### 3. Ordem errada dos artigos
A ordem deve ser **do mais recente ao mais antigo**. O `post.sh` insere o card na posição correta por data. **Correção manual:** reordenar os `<article class="blog-card">` dentro do primeiro `<div class="blog-grid">` por data descendente.

### 4. Botões do hero não clicáveis
Causa: `.hero::before` (overlay decorativo com `inset:0`) interceptava cliques. **Correção:** `.hero::before { pointer-events: none; }`. Confirmar no CSS live: `curl -s <css> | grep -A4 "hero::before"`.

### 5. Cache CDN GitHub Pages (conteúdo antigo no browser)
`expires: max-age=600` + `x-cache: HIT`. **Correção:** forçar atualização com query string `?v=$(date +%s)` nas URLs, ou cache-busting no link do CSS (`style.css?v=YYYYMMDD`).

### 6. Workflow diário falhou
Ver em Actions: `https://github.com/Jorgeacus/marctechja-blog/actions`. Causa comum: falha de timeout/URL da API Gemini (o script só capturava `HTTPError`). **Correção:** tentar manualmente com `workflow_dispatch` (botão "Run workflow"); o `generate-post.py` atual já faz retry nos 4 modelos e 2 versões da API.

### 7. Repo local desatualizado
Sincronizar sempre antes de editar: `git -C ~/MARCS_Blog pull origin main`. Se o repo local estiver atrás do origin e fizer push, regride o site.

## Playbook de resposta

1. **Deteção** — correr `python3 scripts/health-check.py` (ou a checklist manual acima).
2. **Avaliação** — identificar o desvio exato (qual página, qual sintoma, quebra ou só cosmético).
3. **Correção mínima** — resolver só o problema, sem tocar no design, nos artigos ou na estrutura.
4. **Verificação** — repetir o health-check até passar tudo.
5. **Commit + push** — mensagem descritiva do bug corrigido; nunca commitar sem o site verificado.

## Regras de publicação (manter)

- Ordem: mais recente → mais antigo.
- Homepage: só 6 cards (5 essenciais + mais recente) + CTA "Explorar Blog Completo →".
- Blog archive: todos os artigos + formulário Google Forms (iframe) na sidebar.
- Slug: minúsculas, sem acentos, hífens para espaços.
- Autor default: "Hermes Agent" (nunca "MARC-Jarvis").
- **1 artigo por dia**, às 09:00 UTC (workflow "Hermes Agent").
- **Temas:** mistura de Hermes Agent, Python, criação de sites/landing pages, automação (WhatsApp, Telegram, Instagram), gestão de tráfego e redes sociais, análise de mercado/produtos, e conteúdo para micro e grandes empresas. Rotação sequencial em `scripts/generate-post.py` (23 tópicos, do mais simples ao mais complexo) — 1 tema por dia por ordem, reinicia quando chega ao fim. **Não repetir temas/artigos já publicados** — só atualizar ou aprofundar.

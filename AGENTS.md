# MarctechJA — Blog de Hermes Agent

**Domínio:** http://marcusja777.com (HTTPS pendente)  
**GitHub:** Jorgeacus/marctechja-blog (branch `main`)  
**GitHub Pages:** https://jorgeacus.github.io/marctechja-blog/ (redireciona para o domínio)  
**Email:** marctechja@gmail.com

## Como aceder (importante!)
- O site **HTTPS ainda NÃO funciona** (`https://marcusja777.com` dá erro / página em branco). Usar **HTTP**.
- O blog live: `http://marcusja777.com/blog/`
- O GitHub: https://github.com/Jorgeacus/marctechja-blog
- O agente (Hermes Agent / MARC-Jarvis) deve usar `curl http://marcusja777.com/...` para ver o site, não HTTPS.

## Design
- Cores: petróleo `#031522`, navy `#061B2B`, dourado `#D9A83E`, ciano `#008FBE`
- CSS: `assets/css/style.css`

## Páginas
| Página | URL |
|---|---|
| Home (com CTA subscrição) | `/` |
| Blog archive (com formulário subscrição) | `/blog/` |
| Página do Livro | `/livro/` (capa + link Hotmart) |
| Sobre | `/sobre/` |

## Artigos publicados (8)
1. `hermes-agent-skills/` — Skills no Hermes Agent (25 Jul)
2. `hermes-agent-introduction/` — O que é o Hermes Agent (26 Jul)
3. `hermes-agent-automations/` — 5 Automações Diárias (27 Jul)
4. `hermes-agent-installation/` — Como Instalar (28 Jul)
5. `hermes-agent-book-launch/` — Lançamento do ebook (29 Jul)
6. `cria-o-teu-primeiro-assistente-de-estudo-com-hermes-agent/` — Assistente de estudo (29 Jul)
7. `hermes-agent-publica-automaticamente/` — Hermes Agent publica automaticamente (30 Jul)
8. `como-publicar-artigos-com-hermes-agent/` — Como publicar artigos com Hermes Agent (30 Jul)

## SEO
- `sitemap.xml` (PRECISA de ser atualizado — não inclui artigos 6, 7, 8)
- `robots.txt` ativo
- Google AdSense `ca-pub-3717814491008089` (pendente revisão)
- Google Search Console verificado
- `ads.txt` configurado

## Hotmart
- Link: https://hotm.io/jFUussV9 (redireciona para pay.hotmart.com/G106933522A)
- Preço: R$29,90

## Subscrição de leitores
- **Formulário Google Forms** embutido no blog (`/blog/`) via iframe
- Dados (nome, WhatsApp, país, email, canal) vão para a Google Sheet do `marctechja@gmail.com`
- Exportar CSV: Sheet > Ficheiro > Descarregar > CSV
- Link do formulário: https://docs.google.com/forms/d/e/1FAIpQLSfds5NO8081MuTFPXsORTIERAv8WtunDRdgiNdZIq7NKdQalA/viewform
- Homepage tem CTA "Subscrever Grátis" que leva ao formulário

## Scripts de Automação

### `scripts/post.sh`
Publicador automático. Cria HTML, slug (sem espaços), meta tags, atualiza blog archive e homepage, commit+push.

### `scripts/generate-post.py`
Gerador via Gemini API. 10 tópicos rotativos (Hermes Agent, Python/automação, agentes IA). Invoca `post.sh`.

### `scripts/gmail_monitor.py`
Gmail API (ler + responder): `auth`, `search`, `read`, `reply` (draft, NÃO envia), `send`, `unread`, `run`. Duas contas: `radiestesia`, `techja`.

## Workflow GitHub Actions
- **Ficheiro:** `.github/workflows/marc.yml` — **Nome:** "Hermes Agent"
- **Trigger:** `schedule: 0 9 * * *` (09:00 UTC diário) + `workflow_dispatch`
- **Secret:** `GEMINI_API_KEY`
- Pipeline: checkout → setup-python 3.11 → `python3 scripts/generate-post.py`

## API Gemini (2026)
- Endpoint: `https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent`
- Header `x-goog-api-key` (não `?key=`)
- Modelos: `gemini-3.6-flash` (principal), `gemini-2.5-flash-latest`, `gemini-2.5-pro-latest`
- Desde Jun/2026: chaves não restritas devolvem 404.

## Pendente
- ⬜ **HTTPS** — GitHub não emitiu certificado Let's Encrypt para `marcusja777.com`. DNS está correto (4 A records GitHub). Ação: em Settings > Pages, remover e re-adicionar o domínio personalizado.
- ⬜ **Workflow diário** — a execução de 2026-07-30 falhou; a de hoje ainda não correu. Verificar em Actions e acionar manualmente (Run workflow).
- ⬜ **Sitemap** desatualizado (falta artigos 6-8)
- ⬜ Google AdSense — aguardar revisão

## Notas
- MEO (Portugal) bloqueia HTTP — HTTPS resolve.
- Publicação diária: 1 artigo às 09:00 UTC via GitHub Actions (workflow "Hermes Agent").

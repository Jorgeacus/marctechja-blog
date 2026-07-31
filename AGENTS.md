# MarctechJA — Blog de Hermes Agent

**Domínio:** https://marcusja777.com (HTTPS ativo, Let's Encrypt)  
**GitHub:** Jorgeacus/marctechja-blog (branch `main`)  
**GitHub Pages:** https://jorgeacus.github.io/marctechja-blog/ (redireciona para o domínio)  
**Email:** marctechja@gmail.com

## Como aceder (importante!)
- O site **funciona em HTTPS**: `https://marcusja777.com`
- O blog live: `https://marcusja777.com/blog/`
- O GitHub: https://github.com/Jorgeacus/marctechja-blog
- O agente deve usar `curl https://marcusja777.com/...` para ver o site.
- HTTP ainda NÃO redireciona para HTTPS — usar HTTPS sempre.

## Design
- Cores: petróleo `#031522`, navy `#061B2B`, dourado `#D9A83E`, ciano `#008FBE`
- CSS: `assets/css/style.css` (usar `?v=YYYYMMDD` no link para cache-busting)
- **NUNCA alterar o design original** — as correções devem ser mínimas e cirúrgicas.

## Páginas
| Página | URL |
|---|---|
| Home (6 cards + CTA subscrição) | `/` |
| Blog archive (todos os artigos + formulário subscrição) | `/blog/` |
| Página do Livro | `/livro/` (capa + link Hotmart) |
| Sobre | `/sobre/` |

## Artigos publicados (9)
1. `hermes-agent-skills/` — Skills no Hermes Agent (25 Jul)
2. `hermes-agent-introduction/` — O que é o Hermes Agent (26 Jul)
3. `hermes-agent-automations/` — 5 Automações Diárias (27 Jul)
4. `hermes-agent-installation/` — Como Instalar (28 Jul)
5. `hermes-agent-book-launch/` — Lançamento do ebook (29 Jul)
6. `cria-o-teu-primeiro-assistente-de-estudo-com-hermes-agent/` — Assistente de estudo (29 Jul)
7. `hermes-agent-publica-automaticamente/` — Hermes Agent publica automaticamente (30 Jul)
8. `como-publicar-artigos-com-hermes-agent/` — Como publicar artigos com Hermes Agent (30 Jul)
9. `o-que-sao-agentes-de-ia-e-como-funcionam-na-pratica/` — O que são agentes de IA (31 Jul)

**Ordem:** do mais recente para o mais antigo no blog archive. Homepage: 6 cards (5 essenciais + mais recente).

## SEO
- `sitemap.xml` (13 URLs, atualizado automaticamente pelo post.sh)
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

## Agente de manutenção (SKILL)
- **Skill:** `.hermes/skills/devops/marctechja-blog-maintenance/SKILL.md` (versionada no repo)
- **Symlink:** `~/.hermes/skills/devops/marctechja-blog-maintenance` → repo (para o Hermes descobrir)
- **Health check:** `python3 scripts/health-check.py` (verifica HTTP 200, ordenação, comentários HTML, sitemap, cache-busting)
- **Workflow:** `.github/workflows/health-check.yml` — diário 09:30 UTC + manual; cria GitHub Issue automática se detetar quebras

## Scripts de Automação

### `scripts/post.sh`
Publicador automático. Cria HTML, slug, meta tags, atualiza blog archive (ordenado por data) e homepage (máx. 6 cards), sitemap, commit+push.

### `scripts/generate-post.py`
Gerador via Gemini API. 10 tópicos rotativos. Invoca `post.sh`. **Robustez:** tenta 4 modelos × 2 versões da API com retry; captura HTTPError, URLError e timeouts.

### `scripts/reorder-cards.py`
Reordena os cards do blog archive do mais recente ao mais antigo (invocado pelo post.sh).

### `scripts/gmail_monitor.py`
Gmail API (ler + responder): `auth`, `search`, `read`, `reply` (draft, NÃO envia), `send`, `unread`, `run`.

## Workflow GitHub Actions
- **`marc.yml`** — nome "Hermes Agent"; schedule `0 9 * * *` + `workflow_dispatch`; gera e publica 1 artigo/dia
- **`health-check.yml`** — "Health Check Blog"; schedule `30 9 * * *` + `workflow_dispatch`; verifica o site e abre Issue se houver quebras
- **Secret:** `GEMINI_API_KEY`

## API Gemini (2026)
- Endpoint: `https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent`
- Header `x-goog-api-key` (não `?key=`)
- Modelos: `gemini-3.6-flash` (principal), `gemini-2.5-flash-latest`, `gemini-2.5-pro-latest`, `gemini-3.5-flash`
- Desde Jun/2026: chaves não restritas devolvem 404.

## Lições aprendidas
- **BUG CRÍTICO**: Gemini gerou `<!-- SEO Metadata ... -->`; o truncamento com `head -c` deixava `<!--` sem fecho → navegador tratava o resto como comentário (1 artigo visível). **Correção:** `re.sub(r"<!--.*?-->", "", raw, DOTALL)` em SEO_DESC/EXCERPT/EXCERPT_HOME; prompt proíbe comentários.
- **Botões do hero**: `.hero::before` (overlay `inset:0`) interceptava cliques → `pointer-events: none`.
- **Cache CDN**: GitHub Pages usa `max-age=600` + `x-cache: HIT` → forçar `?v=...` nas URLs e cache-busting no CSS.
- **Falha da API**: o script só capturava `HTTPError`; timeouts/URLError falhavam sem retry → agora captura tudo e tenta 4 modelos com retry.
- **Repo local em `~/MARCS_Blog`** (NUNCA /tmp — é apagado ao reiniciar). Fazer `git pull` antes de editar.

## Pendente
- ⬜ HTTP→HTTPS: sugerir "Enforce HTTPS" em Settings > Pages (o HTTP ainda não redireciona)
- ⬜ Google AdSense — aguardar revisão
- ⬜ Exportar subscritores da Sheet para `subscribers.csv` quando houver dados

## Notas
- A automação do blog vive 100% no GitHub Actions (runner efémero) — não há dependência de /tmp local.
- Publicação diária: 1 artigo às 09:00 UTC via workflow "Hermes Agent".

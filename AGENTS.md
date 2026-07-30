# MarctechJA — Blog MARC-Jarvis

**Domínio:** https://marcusja777.com  
**GitHub:** Jorgeacus/marctechja-blog (branch `main`)  
**GitHub Pages:** https://jorgeacus.github.io/marctechja-blog/  

## Design
- Cores Hermes: petróleo `#031522`, navy `#061B2B`, dourado `#D9A83E`, ciano `#008FBE`
- CSS: `assets/css/style.css`
- Fonte: system-ui sans-serif

## Páginas
| Página | URL |
|---|---|
| Home | `/` |
| Blog archive | `/blog/` |
| Página do Livro | `/livro/` (com capa + link Hotmart) |
| Artigos | `/blog/<slug>/` |

## Estrutura de artigos publicados
1. `hermes-agent-introducao/` — Introdução ao Hermes Agent
2. `hermes-agent-book-launch/` — Lançamento do ebook
3. `instalar-hermes-agent/` — Instalação
4. `primeiras-automacoes/` — Primeiras automações
5. `criar-skills-hermes-agent/` — Criar skills
6. `cria-o-teu-primeiro-assistente-de-estudo-com-hermes-agent/` — (GERADO PELO MARC-JARVIS em 2026-07-29)

## SEO
- `sitemap.xml` com 9+ URLs
- `robots.txt` ativo
- Open Graph + meta tags em todas as páginas
- Google AdSense `ca-pub-3717814491008089` (pendente revisão)
- Google Search Console verificado
- `ads.txt` configurado

## Hotmart
- Link: https://hotm.io/jFUussV9 (redireciona para pay.hotmart.com/G106933522A)
- Preço: R$29,90
- Botões: página do livro (2x) + artigo de lançamento (1x)

## Scripts de Automação

### `scripts/post.sh`
Publicador automático de artigos. Cria HTML, slug, atualiza blog archive e homepage, faz git commit+push.

### `scripts/generate-post.py`
Gerador de conteúdo via Gemini API:
- 10 tópicos pré-definidos (universitários, ensino médio, professores, criadores, WhatsApp, email)
- Referência: `assets/reference/ebook-summary.md` (para a IA)
- Invoca `post.sh` após gerar conteúdo
- Fallback: tenta `v1` → `v1beta`, vários modelos Gemini

### `scripts/gmail_monitor.py`
Assistente de Gmail via API Google (ler + responder):
- `auth` — Autenticação OAuth 2.0 (primeira vez)
- `search --query "palavra"` — Pesquisar emails
- `read --id <msg_id>` — Ler conteúdo completo do email
- `reply --id <msg_id> --body "..."` — Cria rascunho, **mostra no ecrã, NÃO envia**
- `send --to "x" --subject "y" --body "z"` — Enviar email (só após aprovação)
- `send-draft --id <draft_id>` — Enviar rascunho existente
- `unread` — Ver não lidas
- `run` — Relatório JSON completo
- **Fluxo seguro**: `reply` só cria draft + mostra; utilizador aprova antes de `send`
- Requer OAuth 2.0 com scopes `gmail.readonly + gmail.send + gmail.compose + gmail.modify`
- Automação: definir `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`

## Workflow GitHub Actions

**Ficheiro:** `.github/workflows/marc.yml`  
**Nome:** MARC-Jarvis  
**Trigger:** `schedule: 0 9 * * *` + `workflow_dispatch`  
**Permissão:** `contents: write`  
**Secret:** `GEMINI_API_KEY` (Google Gemini API key, restrita ao Gemini API)

### Pipeline
1. `actions/checkout@v4`
2. `actions/setup-python@v5` (3.11)
3. `python3 scripts/generate-post.py`

## API Gemini (2026)

**Endpoint:** `https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent`  
**Autenticação:** Header `x-goog-api-key` (não query param `?key=`)  
**Modelos atuais:** `gemini-3.6-flash`, `gemini-2.5-pro-latest`, `gemini-2.5-flash-latest`  
**Modelos deprecated/removidos (2026):** `gemini-1.5-*`, `gemini-1.0-pro`, `gemini-2.0-*`  
**Nota:** Desde Junho 2026, chaves não restritas devolvem 404. Criar chave em `https://aistudio.google.com/app/apikey`

## Lições Aprendidas (2026-07-29)

1. **Workflow dispatch 422**: Sucede a renomear ficheiros workflow. Solução: apagar `.github/` inteiro e recriar de raiz.
2. **Gemini API 404**: Modelos `gemini-1.5-*` foram removidos em 2026. Usar `gemini-3.6-flash` + header `x-goog-api-key`.
3. **Chave API restrita**: A partir de 19 Junho 2026, Gemini API rejeita chaves não restritas (devolve 404). Gerar nova chave em AI Studio.

## Pendente
- ⬜ HTTPS ativo em `https://marcusja77.com` (SSL GitHub em provisionamento — aguardar até 24h)
- ⬜ Google AdSense — aguardar revisão (1-7 dias)
- ⬜ Google Analytics (opcional)

## Notas
- MEO (Portugal) bloqueia HTTP — o site só ficará acessível a todos quando o SSL estiver ativo
- MARC-Jarvis publica automaticamente 1 artigo/dia às 9:00 UTC via GitHub Actions
- Workflow: `.github/workflows/marc.yml`

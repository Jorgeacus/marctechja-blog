# MarctechJA — Blog de Hermes Agent

**Domínio:** https://marcusja777.com (HTTPS ativo)  
**GitHub:** Jorgeacus/marctechja-blog (branch `main`) — repo de origem/versionamento  
**Alojamento (desde 6 Ago 2026):** Cloudflare Pages (`marctechja-blog.pages.dev`) + DNS na Cloudflare. Deploy diário via GitHub Actions → `wrangler pages deploy` (Direct Upload) — **não** depende da fila do GitHub Pages.  
**GitHub Pages:** desativado como origem do domínio (o domínio aponta para o Cloudflare Pages).  
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
- **Cache-busting do CSS é AUTOMÁTICO:** `scripts/post.sh` deriva a versão do último commit que tocou em `style.css` e sincroniza `?v=` em TODAS as páginas (artigos, arquivo, home, legais, 404) a cada publicação. **NUNCA** editar a versão `?v=` à mão — basta editar o CSS e commitar; a próxima publicação normaliza tudo. O `health-check.py` valida a consistência (local e live).
- **NUNCA alterar o design original** — as correções devem ser mínimas e cirúrgicas.

## Páginas
| Página | URL |
|---|---|
| Home (6 cards + CTA subscrição) | `/` |
| Blog archive (todos os artigos + formulário subscrição) | `/blog/` |
| Página do Livro | `/livro/` (capa + link Hotmart) |
| Sobre | `/sobre/` |
| Política de Privacidade | `/politica-de-privacidade/` |
| Política de Cookies | `/politica-de-cookies/` |
| Termos de Uso | `/termos/` |
| Contactos | `/contactos/` |

**Páginas legais (Privacidade, Cookies, Termos, Contactos) são OBRIGATÓRIAS para a aprovação do Google AdSense** — não remover.
- **Guia Destacado FIXO na Home (13 Ago):** a homepage tem um bloco `.featured-guide` (estilo `assets/css/style.css`) logo após o hero, que liga a `/blog/como-aproveitar-os-exemplos-praticos-do-blog-ao-maximo/`. Este bloco está **FORA do `<div class="blog-grid">`** e usa classes próprias (não `blog-card`), por isso o `post.sh` (que insere no grid e corta o card mais antigo) e o `sync-css-version.sh` **nunca o removem nem alteram**. Para atualizar o guia: editar o artigo (`blog/como-aproveitar-os-exemplos-praticos-do-blog-ao-maximo/index.html`) e, se mudar texto/ligação na Home, o bloco `<div class="featured-guide">` em `index.html`. Não mover o bloco para dentro do `blog-grid`.
- **Banner de consentimento de cookies (CMP ligeiro):** `assets/js/cookie-consent.js` + CSS no fim de `style.css`. Adicionar a tag `<script src="/assets/js/cookie-consent.js"></script>` após `main.js` em **qualquer página nova**. O template em `scripts/post.sh` já a inclui.

## Artigos publicados (15)
1. `hermes-agent-skills/` — Skills no Hermes Agent (25 Jul)
2. `hermes-agent-introduction/` — O que é o Hermes Agent (26 Jul)
3. `hermes-agent-automations/` — 5 Automações Diárias (27 Jul)
4. `hermes-agent-installation/` — Como Instalar (28 Jul)
5. `hermes-agent-book-launch/` — Lançamento do ebook (29 Jul)
6. `cria-o-teu-primeiro-assistente-de-estudo-com-hermes-agent/` — Assistente de estudo (29 Jul)
7. `hermes-agent-publica-automaticamente/` — Hermes Agent publica automaticamente (30 Jul)
8. `como-publicar-artigos-com-hermes-agent/` — Como publicar artigos com Hermes Agent (30 Jul)
9. `o-que-sao-agentes-de-ia-e-como-funcionam-na-pratica/` — O que são agentes de IA (31 Jul)
10. `automatizar-mensagens-no-whatsapp-com-hermes-agent/` — Automatizar mensagens no WhatsApp (1 Ago)
11. `criar-uma-landing-page-simples-com-html-e-css-em-30-minutos/` — Criar uma landing page com HTML e CSS (2 Ago)
12. `automatizar-o-telegram-com-hermes-agent-respostas-e-agendamentos/` — Automatizar o Telegram (4 Ago)
13. `automatizar-o-atendimento-no-whatsapp-business-com-hermes-agent/` — WhatsApp Business (5 Ago)
14. `criar-uma-landing-page-para-o-teu-produto-com-html-e-css/` — Landing page para o teu produto (6 Ago)
15. `enviar-audio-e-imagens-automaticos-no-whatsapp-com-hermes-agent/` — Enviar áudio e imagens no WhatsApp (7 Ago)

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
Gerador via Gemini API. 23 tópicos rotativos (do mais simples ao mais complexo): WhatsApp, landing pages, Python, Telegram, Instagram, gestão de tráfego e redes sociais, análise de mercado/produtos, micro e grandes empresas, etc. **Rotação sequencial por dia** (1 tema/dia, por ordem, começando a 1 Ago 2026) — não aleatória. Sem repetição de artigos já publicados. Invoca `post.sh`. **Robustez:** tenta 4 modelos × 2 versões da API com retry; captura HTTPError, URLError e timeouts. **Validação de qualidade:** `validate_content()` corre antes de publicar — rejeita artigos truncados (tags <pre> partidas, conteúdo cortado a meio), com comentários HTML, com <h1> no corpo ou com o título repetido no primeiro <h2>; tenta gerar de novo e aborta se falhar 2×. Autor: "Hermes Agent" (nunca MARC-Jarvis).

### `scripts/reorder-cards.py`
Reordena os cards do blog archive do mais recente ao mais antigo (invocado pelo post.sh).

### `scripts/gmail_monitor.py`
Gmail API (ler + responder): `auth`, `search`, `read`, `reply` (draft, NÃO envia), `send`, `unread`, `run`.

### `scripts/sync-css-version.sh`
Sincroniza o cache-busting do CSS (`?v=YYYYMMDD`) em TODAS as páginas HTML para a versão atual do `style.css` (derivada do git). Idempotente. Usado pelo `post.sh` a cada publicação e pelo agente de manutenção (`repair.yml`, ação `sync_css`).

### `scripts/repair-agent.py`
Sub-agente de classificação do agente de manutenção. Recebe o log de um run falhado + contexto git e devolve `ACTION=`/`DIAG=` (stdout) usando Gemini com um **conjunto fechado** de ações: `regenerate | sync_css | nothing | issue`. Qualquer falha (sem chave, API fora do ar, resposta inválida, ação fora do conjunto) cai para `issue` — nunca age fora do permitido.

## Workflow GitHub Actions
- **`marc.yml`** — nome "Hermes Agent"; schedule `0 9 * * *` + `workflow_dispatch`; gera e publica 1 artigo/dia (gera com Gemini, commita+push para o repo, e **deploys para o Cloudflare Pages** via `cloudflare/wrangler-action@v3` com `wrangler pages deploy _site --project-name=marctechja-blog --branch=production`)
- **`health-check.yml`** — "Health Check Blog"; schedule `30 9 * * *` + `workflow_dispatch`; verifica o site e abre Issue se houver quebras
- **`repair.yml`** — "Manutenção Automática" (agente híbrido); gatilho `workflow_run` quando "Hermes Agent" ou "Health Check Blog" terminarem **com falha** + `workflow_dispatch`; descarrega o log real do run falhado, classifica com `repair-agent.py` e executa:
  - `regenerate`: reexecuta `generate-post.py` (portão: `health-check.py --local`)
  - `sync_css`: normaliza `?v=` em todas as páginas (portão: `health-check.py --local`) e commita como "Manutenção Automática"
  - `nothing`: sem ação (falha transitória)
  - `issue`: **abre Issue para humano** (erro de lógica/design/situação ambígua — nunca altera o design original)
  - Guardrails: `concurrency` impede reparações simultâneas; o `repair.yml` NÃO se auto-gatilha (não está na lista monitorizada) → sem loops; máx. 1 reparação por evento.
- **Secrets:** `GEMINI_API_KEY`, `CLOUDFLARE_API_TOKEN` (permissão Pages:Edit), `CLOUDFLARE_ACCOUNT_ID`

## Cloudflare Pages (alojamento desde 6 Ago 2026)
- Projeto: `marctechja-blog` (Direct Upload — sem build). URL: `marctechja-blog.pages.dev`. Domínio custom: `marcusja777.com`.
- O deploy NÃO passa pela fila do GitHub Pages: `wrangler pages deploy _site` envia os ficheiros via API (instântaneo). `scripts/stage-site.sh` prepara `_site/` (rsync com exclusões de `.github`, `scripts`, `AGENTS.md`, `subscribers.csv`, etc.) — o wrangler direct upload NÃO suporta `.assetsignore` (isso é só Workers Assets), por isso usamos staging.
- DNS: o domínio está no plano grátis da Cloudflare (nameservers da Cloudflare na Hostinger). Recorde `marcusja777.com` CNAME (flattened) → `marctechja-blog.pages.dev`, proxy ativado. HTTPS universal (certificado auto da Cloudflare).
- **Migração (checklist manual, 6 Ago — CONCLUÍDA):**
  - [x] Conta Cloudflare (grátis) + zona `marcusja777.com` adicionada (agora `active`, id `8cb322bc8c0e8a68c07e15d339db35fc`).
  - [x] API Token `cfat_1wKE…5311` (Account » Cloudflare Pages » Edit; sem permissão DNS — recordes geridos manualmente no painel).
  - [x] Projeto Pages `marctechja-blog` (Direct Upload) + 1º deploy (`bash scripts/stage-site.sh && npx wrangler pages deploy _site --project-name=marctechja-blog`) — `marctechja-blog.pages.dev` e `marcusja777.com` live; `scripts/AGENTS.md/subscribers.csv` → 404.
  - [x] Domínio custom `marcusja777.com` atachado e validado (verification `active`; cert Google Trust Services até 4 Nov).
  - [x] Hostinger: nameservers trocados para `nelly.ns.cloudflare.com` + `zahir.ns.cloudflare.com` (zona `active`).
  - [x] Recorde DNS: apex `marcusja777.com` **CNAME → `marctechja-blog.pages.dev`** (com proxy). ⚠️ criar no painel DNS → Records com Name `@`; um CNAME com Name `www` NÃO valida o domínio (Pages devolve "CNAME record not set").
  - [x] Secrets GitHub `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` definidos (PUT 201, 6 Ago).
  - [x] GitHub Pages desativado: Settings → Pages → Source "Deploy from a branch" (PUT `/pages` 204) — acaba o workflow auto "pages build and deployment".
  - [x] Verificado: `python3 scripts/health-check.py` (live) 100% OK, `server: cloudflare`, HTTP→HTTPS 301, cert válido.

## API Gemini (2026)
- Endpoint: `https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent`
- Header `x-goog-api-key` (não `?key=`)
- Modelos: `gemini-3.6-flash` (principal), `gemini-2.5-flash-latest`, `gemini-2.5-pro-latest`, `gemini-3.5-flash`
- Desde Jun/2026: chaves não restritas devolvem 404.

## Lições aprendidas
- **BUG CRÍTICO**: Gemini gerou `<!-- SEO Metadata ... -->`; o truncamento com `head -c` deixava `<!--` sem fecho → navegador tratava o resto como comentário (1 artigo visível). **Correção:** `re.sub(r"<!--.*?-->", "", raw, DOTALL)` em SEO_DESC/EXCERPT/EXCERPT_HOME; prompt proíbe comentários.
- **Botões do hero**: `.hero::before` (overlay `inset:0`) interceptava cliques → `pointer-events: none`.
- **Cache CDN**: GitHub Pages usa `max-age=600` + `x-cache: HIT` → forçar `?v=...` nas URLs e cache-busting no CSS.
- **Responsividade mobile (6 Ago)**: artigos alargavam-se para o lado no iPhone porque o grid `.layout-with-sidebar { grid-template-columns: 1fr 300px }` não encolhia abaixo do min-content e havia `<code>`/URLs longos que não quebravam. **Correção no `style.css`:** `grid-template-columns: minmax(0, 1fr) 300px` + `min-width: 0` nos filhos, `overflow-wrap: anywhere` em `code`/`a`, `overflow-x: clip` no html/body, `table { display:block; overflow-x:auto }` e `overflow-wrap` em headings. **Automação:** versão CSS derivada de git + sincronização global no `post.sh`; `health-check.py` valida que todas as páginas usam a mesma versão e que o CSS live tem as proteções.
- **Falha de publicação (6 Ago)** — causa confirmada pelo log real do run: o artigo daquele dia (landing page, muito HTML/CSS) excedia `maxOutputTokens: 4096`, a API cortava a meio de um `<pre>`, a validação rejeitava e com só 2 tentativas o run falhava (a chave GEMINI_API_KEY do Actions **estava válida** — os `404` de `gemini-2.5-*-latest` eram modelos mortos, o `503` era transitório). **Correções:** `maxOutputTokens: 8192`; até **3 tentativas** de regeneração na validação; guarda que salta tópicos já publicados em `blog/`; modelos reordenados (3.6-flash e 3.5-flash primeiro); `python3 scripts/generate-post.py --dry-run` para gerar+validar SEM publicar.
- **Propagação de erros no post.sh (6 Ago)**: o `post.sh` engolia falhas de `git commit`/`git push` e devolvia sempre exit 0 — o `generate-post.py` reportava sucesso mesmo sem publicar. **Correção:** agora devolve exit 1 se o push falhar, e faz verificação pós-publicação (aguarda o artigo responder HTTP 200 no deploy do Pages, até `VERIFY_ATTEMPTS` × 20s; avisa sem falhar — o health-check diário é a rede de segurança).
- **RoTAÇÃO ESGOTADA → artigo duplicado (19 Ago)**: os dispatches de deploy do `marc.yml` (usados para publicar correções da landing) **também correm `generate-post.py` e publicam artigos** — cada dispatch consome um tópico da rotação. Como houve 4 dispatches num dia, os 23 tópicos esgotaram e o cron seguinte caiu no fallback `TOPICS[today_index % len]`, que **re-publicava um tópico já existente** → criava um 2º card duplicado no archive e sobrescrevia o `datePublished` do artigo (17 Ago→19 Ago). **Correções:** (1) o fallback agora faz `exit 0` quando todos os tópicos já foram publicados (nunca re-publica um existente); (2) `TOPICS` expandido de 23 para 33 (SEO, scraping, newsletter, CRM, etc.). Para corrigir um duplicado no archive: remover o card antigo de `blog/index.html` e o `<url>` repetido em `sitemap.xml` (o `post.sh`/`reorder-cards.py` não deduplicam).
- **Falha da API**: o script só capturava `HTTPError`; timeouts/URLError falhavam sem retry → agora captura tudo e tenta 4 modelos com retry.
- **BUG `\n` literal nos cards**: `NEW_CARD+="\n..."` em bash com aspas duplas produz os caracteres literais `\`+`n` (não quebra de linha). **Correção:** usar `$'\n'` (ANSI-C quoting) nas construções de NEW_CARD/NEW_CARD_HOME. Sintomas: `\n` visível no card da homepage/blog. Verificado com `od -c`.
- **Título duplicado**: o Gemini às vezes repete o título como primeiro `<h2>` do corpo → meta description e card ficam com o título 2×. **Correção:** prompt do generate-post.py proíbe repetir o título; EXCERPT/EXCERPT_HOME no post.sh ignoram o primeiro heading se for igual ao título.
- **ARTIGO TRUNCADO (landing page, 2 Ago)**: o Gemini cortou o artigo a meio do Passo 2 (parágrafo "adaptado a" sem fim) e saltou direto para o CTA do livro — corpo pela metade, meta description também cortada com aspas não escapadas. **Correção (2 níveis):** (1) manual — completado o CSS, Passos 3-4, conclusão e meta; (2) automática — `validate_content()` no generate-post.py deteta conteúdo cortado/blocos <pre> partidos antes de publicar e regera.
- **Código Python quebrado (skills, 25 Jul)**: bloco `AnalisarSentimento` chamava `self.analyze()` que nunca estava definido (daria AttributeError). **Regra:** todo o código apresentado tem de executar sem erro (verificar métodos/imports). **Corrigido** com implementação real (contagem de palavras positivas/negativas).
- **Formato de skill inconsistente entre artigos**: usavam `.yaml` com `inputs/steps/action`, `llm.generate`, `tools.*` e `hermes run` — **não existe** no Hermes Agent v0.17.0. **Correção:** uniformizado para o FORMATO CANÓNICO real — `SKILL.md` (frontmatter + Markdown narrativo) + `hermes chat -s <skill>` / `hermes skills list`. Prompt do generate-post.py exige este formato.
- **Comando de instalação errado**: artigos usavam `brew install hermes-agent` e `pip install hermes-agent`, mas o instalador oficial é `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash` (macOS/Linux) e `iex (irm https://hermes-agent.nousresearch.com/install.ps1)` (Windows). **Regra:** instalação = instalador oficial; nunca `brew install` nem `pip install`.
- **Meta description truncada**: várias metas cortavam a meio (`... respo"`) ou começavam com o título repetido. **Regra:** meta description completa, com pontuação final, sem repetir o título e sem aspas não escapadas.
- **Repo local em `~/MARCS_Blog`** (NUNCA /tmp — é apagado ao reiniciar). Fazer `git pull` antes de editar.
- **Agente de manutenção híbrido (6 Ago)**: a classificação de falhas por IA tem de usar um **conjunto fechado de ações** e cair SEMPRE para `issue` em caso de ambiguidade/falha da API — nunca auto-corrigir sem portão de verificação (`health-check.py --local`). O contexto git (últimos commits) no prompt é essencial: evitou que o agente re-publicasse um artigo que já tinha sido publicado manualmente (classificou `nothing` em vez de `regenerate`). Modelos flash podem ecoar o system prompt e esgotar o output a meio do JSON → maxOutputTokens generoso (1200) + extração de `action` por regex como fallback. YAML do Actions: conteúdo de `run: |` tem de estar indentado (o `BODY` multi-linha da Issue sem indentação quebra o parse).
- **Deploy do Pages preso na fila (6 Ago)**: o workflow auto-gerado "pages build and deployment" falhou 3× seguidas com `actions/deploy-pages` a atingir o timeout de 600s — o build/upload do artefacto passou, o deployment foi criado mas ficou **`deployment_queued`** para sempre (fila do Pages presa). É **infraestrutura do GitHub, sem fix no repositório**; o site manteve-se live com a versão anterior (health-check passa). Ação: re-run do run falhado (ou novo push) para re-encolar o deployment; se persistir, esperar — nunca alterar código por causa disto.
- **`secrets` NÃO é permitido em condições `if:` (7 Ago)**: `if: ${{ secrets.X != '' }}` invalida o workflow inteiro (`Unrecognized named-value: 'secrets'`) → o cron não dispara, o `workflow_dispatch` devolve 422 e os pushes criam runs de validação com 0 jobs que falham. **Correção:** expor o secret num `env` a nível do job (`CF_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}`) e usar `if: env.CF_API_TOKEN != ''` no passo — o contexto `env` é válido em `if:`. Deteção: se o `marc.yml` não correr no horário e o dispatch der 422, validar o ficheiro com o parser do GitHub (o PyYAML local não apanha este erro — só o parser do GitHub).
- **Papel do token Cloudflare ≠ solução das falhas de publicação (13 Ago)**: o `CLOUDFLARE_API_TOKEN` (`cfat_`, Pages:Edit) é **só uma credencial do passo de deploy** do `marc.yml` (introduzida com a migração para Cloudflare Pages) — **não** corrigiu nem causou as falhas diárias de geração/publicação (essas foram `maxOutputTokens`, modelos Gemini mortos, `validate_content`, propagação de erros do `post.sh`, `secrets` em `if:`). **Deploy é 100% automatizado no GitHub Actions** (cron `0 9 * * *` + dispatch) e funciona há 7+ dias consecutivos — a publicação diária **não depende do Mac nem de tokens locais**.
- **Deploy local via wrangler exige token com Pages:Edit (13 Ago)**: o token no `.zshrc` (`cfut_`, len ~53) valida a identidade na API (verify 200) mas **não tem permissão Cloudflare Pages:Edit** → `wrangler pages deploy` falha com `Authentication error [code: 10000]`. O token com permissão (`cfat_`) está **apenas como secret do GitHub** (não localmente). **Procedimento definitivo para publicar correções:**
  1. `git pull --rebase` + commit + push (o remoto pode ter avançado — rebase antes de push).
  2. Disparar o deploy pelo GitHub Actions: `gh workflow run marc.yml` (se `gh` instalado) **ou** via API com o PAT do keychain: `git credential-osxkeychain get` (protocol=https, host=github.com) → `password` = token; `POST /repos/Jorgeacus/marctechja-blog/actions/workflows/marc.yml/dispatches` com `{"ref":"main"}` (HTTP 204 = aceite). ⚠️ O `marc.yml` gera um artigo novo **e** faz deploy — é o comportamento normal (publicação diária).
  3. Opcional (deploy manual local): substituir o token `cfut_` do `.zshrc` pelo `cfat_` (Pages:Edit) — guardar com cuidado por ter escrita no Pages.
  4. Validar com `python3 scripts/health-check.py` (live) e conferir o conteúdo corrigido no site (ex: `curl https://marcusja777.com/blog/hermes-agent-installation/` não deve conter `brew install hermes-agent`).

## Regras de estrutura e qualidade dos artigos
Estas regras são OBRIGATÓRIAS para qualquer artigo (gerado ou editado manualmente):

### Estrutura didática
1. **Introdução curta** que desperta interesse ("Imagina...", "Sentes que...") antes do primeiro heading.
2. **Passos numerados** ("Passo 1:", "Passo 2:", ...) para tutoriais práticos, cada um com: explicação + código + explicação do código.
3. **Conclusão** que resuma o que o leitor aprendeu + próximo passo sugerido.
4. **Artigo completo** — nunca deixar parágrafo, lista ou bloco de código cortado a meio.

### Qualidade de código
5. **Código funcional**: verificar mentalmente que executa (sintaxe, indentação, métodos definidos, imports). Nunca mostrar código que daria erro.
6. **Formato canónico de skill (usar SEMPRE)** — skills são ficheiros `SKILL.md` em Markdown, com frontmatter YAML e corpo narrativo (NUNCA ficheiros `.yaml` com `inputs/steps/action`):
   ```markdown
   ---
   name: <nome>
   description: <o que faz>
   author: MarctechJA
   version: "1.0"
   platforms:
     - macos
     - linux
     - windows
   metadata:
     hermes:
       tags: [<tag1>, <tag2>]
   ---

   # <nome>

   <Descrição curta do que a skill faz>

   ## When to Use
   <Quando usar esta skill>

   ## Instruções
   1. <Passo 1 — o que o agente deve fazer>
   2. <Passo 2>

   ## Critérios de conclusão
   - <Condição de fim bem-sucedido>
   ```
   - Caminho real: `~/.hermes/skills/<nome>/SKILL.md` (uma pasta por skill).
   - Execução real: `hermes skills list` e `hermes chat -s <nome>` (NUNCA `hermes run`).
   - Referência canónica: `~/.hermes/hermes-agent/skills/software-development/hermes-agent-skill-authoring/SKILL.md`.
7. **Instalação**: macOS e Linux — `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`; Windows (PowerShell) — `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`. Nunca `brew install hermes-agent` nem `pip install hermes-agent` (não são oficiais).
8. **Não inventar URLs**: usar apenas os repositórios/links oficiais conhecidos.

### Limpeza
9. **Sem comentários HTML** (`<!-- -->`) no corpo — removidos na publicação e quebram validação.
10. **Sem `<h1>` no corpo** — headings internos começam em `<h2>`.
11. **Não repetir o título** como primeiro heading ou na meta description (evita duplicação em excerpts/cards).
12. **Meta description completa**, com pontuação final, sem aspas não escapadas e sem cortes.

### Verificação antes de publicar
- Correr `python3 scripts/health-check.py` (valida 200s, ordenação, comentários, sitemap, cards).
- Os artigos gerados passam por `validate_content()` (generate-post.py) antes do push — se falhar, regenera.

## Pendente
- ⬜ **AdSense** — primeira revisão reprovada. Corrigido: páginas Privacidade, Cookies, Termos e Contactos + links no footer + sitemap + **banner de consentimento de cookies (CMP)** (4 Ago). **Artigos finos reforçados para ≥800 palavras** (4 Ago): hermes-agent-automations (804), book-launch (801), installation (815), introduction (963), publica-automaticamente (871), como-publicar-artigos (844) — com secções novas úteis (FAQ, conclusões, exemplos, workflows). Pedir nova revisão quando publicado.
  - **Descobertas da pesquisa AdSense (4 Ago):**
    - A meta tag `<meta name="google-adsense-account" content="ca-pub-...">` É o método recomendado de código AdSense — já está em todas as 20 páginas (404.html e ficheiro de verificação do Google excetuados). NÃO adicionar o script `adsbygoogle.js`/unidades de anúncio até a revisão aprovar.
    - Revisão "site not ready" foca: conteúdo único/original, navegação clara, UX; Google **sugere secção de comentários** (moderada) — não implementada ainda (candidata).
    - CMP certificado Google + TCF é OBRIGATÓRIO para servir **anúncios personalizados** a utilizadores EEA/Reino Unido/Suíça (desde 16 Jan 2024). O banner atual é um CMP ligeiro próprio — se a revisão aprovar e formos servir anúncios na UE, considerar CMP certificado (Google "Privacy & messaging" ou terceiro TCF) ou servir apenas anúncios não personalizados.
    - Sem links partidos, páginas legais presentes, HTTPS ok, sitemap sem `lastmod` (melhoria opcional).
  - **Melhorias adicionais (4 Ago, auditoria profunda):** JSON-LD (WebSite/Organization/Organization+BlogPosting) em home, sobre e todos os artigos + template post.sh; `<meta name="author">` e byline "✍️ Hermes Agent" em todos os artigos; página Sobre com identidade do autor (Marcus/GitHub Jorgeacus); Privacidade+Cookies com `aboutads.info` e menção ao banner; divulgação de afiliados nos Termos (4.1) e no livro; `<lastmod>` no sitemap; link "Definições de cookies" no rodapé (reabre o banner via `window.MarctechJACookieConsent.show()`).
- ⬜ Exportar subscritores da Sheet para `subscribers.csv` quando houver dados

## MARC-Jarvis (agente local) — papel no blog
- **Papel:** Editor/Consultor/Administrador (NUNCA autor — autor é sempre "Hermes Agent").
- **Regras gravadas em:** `memory/long_term.json` (Mark-XLVII) + `core/prompt.txt` (protocolo).
- **Regras:** 1 artigo/dia ao ligar o Mac; nunca assumir "novo dia" só por reinício; consultar `notes.blog_artigos_publicados` antes de gerar (não repetir temas); formato/cores Hermes intocáveis; CTAs ebook + subscrição; páginas legais; AdSense `ca-pub-3717814491008089`.
- **Ebook (PDF):** `/Volumes/MacWinGamer/Hermes-Ebook-MYRA/Hermes_Agent_Ebook_MarcTechJA.pdf`.
- **Aviso:** o MARC-Jarvis local NÃO tem ferramenta de git/push — a publicação diária vive no GitHub Actions. Ele edita/reve/administra localmente e atualiza a lista de publicados na memória.
- **Arranque:** `com.marc.jarvis` (launchd, RunAtLoad) + `ai.hermes.gateway` (Hermes, RunAtLoad). Epic Games desabilitado (`com.epicgames.launcher.plist.disabled`).

## Notas
- A automação do blog vive 100% no GitHub Actions (runner efémero) — não há dependência de /tmp local.
- Publicação diária: 1 artigo às 09:00 UTC via workflow "Hermes Agent".
- Temas: Hermes Agent + Python + criação de sites/landing pages + automação (WhatsApp, Telegram, Instagram) + gestão de tráfego e redes sociais + análise de mercado/produtos + micro e grandes empresas, em rotação sequencial diária (sem repetir publicados).

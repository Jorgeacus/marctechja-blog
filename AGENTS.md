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
| Política de Privacidade | `/politica-de-privacidade/` |
| Política de Cookies | `/politica-de-cookies/` |
| Termos de Uso | `/termos/` |
| Contactos | `/contactos/` |

**Páginas legais (Privacidade, Cookies, Termos, Contactos) são OBRIGATÓRIAS para a aprovação do Google AdSense** — não remover.
- **Banner de consentimento de cookies (CMP ligeiro):** `assets/js/cookie-consent.js` + CSS no fim de `style.css`. Adicionar a tag `<script src="/assets/js/cookie-consent.js"></script>` após `main.js` em **qualquer página nova**. O template em `scripts/post.sh` já a inclui.

## Artigos publicados (11)
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
- **BUG `\n` literal nos cards**: `NEW_CARD+="\n..."` em bash com aspas duplas produz os caracteres literais `\`+`n` (não quebra de linha). **Correção:** usar `$'\n'` (ANSI-C quoting) nas construções de NEW_CARD/NEW_CARD_HOME. Sintomas: `\n` visível no card da homepage/blog. Verificado com `od -c`.
- **Título duplicado**: o Gemini às vezes repete o título como primeiro `<h2>` do corpo → meta description e card ficam com o título 2×. **Correção:** prompt do generate-post.py proíbe repetir o título; EXCERPT/EXCERPT_HOME no post.sh ignoram o primeiro heading se for igual ao título.
- **ARTIGO TRUNCADO (landing page, 2 Ago)**: o Gemini cortou o artigo a meio do Passo 2 (parágrafo "adaptado a" sem fim) e saltou direto para o CTA do livro — corpo pela metade, meta description também cortada com aspas não escapadas. **Correção (2 níveis):** (1) manual — completado o CSS, Passos 3-4, conclusão e meta; (2) automática — `validate_content()` no generate-post.py deteta conteúdo cortado/blocos <pre> partidos antes de publicar e regera.
- **Código Python quebrado (skills, 25 Jul)**: bloco `AnalisarSentimento` chamava `self.analyze()` que nunca estava definido (daria AttributeError). **Regra:** todo o código apresentado tem de executar sem erro (verificar métodos/imports). **Corrigido** com implementação real (contagem de palavras positivas/negativas).
- **Formato de skill YAML inconsistente entre artigos**: uns usavam `parameters:` outros `inputs:`; uns `{var}` outros `{{ inputs.var }}`; uns `type: tool` + `steps/action`, outros `steps/prompt`. **Correção:** uniformizado para o FORMATO CANÓNICO — `name`/`description`/`author`/`version` + `inputs:` (tipo/descrição/required) + `steps:` com `name`/`action`/`params` (referências `{{ inputs.x }}` e `{{ steps.x.output }}`) + `outputs:`. Prompt do generate-post.py exige este formato.
- **Comando de instalação inconsistente**: artigo de estudo usava `pip install hermes-agent`, mas o guia oficial usa `brew install hermes-agent` (macOS) / git clone+venv (Linux/Windows). **Regra:** instalação macOS = `brew install hermes-agent`; nunca `pip install hermes-agent`.
- **Meta description truncada**: várias metas cortavam a meio (`... respo"`) ou começavam com o título repetido. **Regra:** meta description completa, com pontuação final, sem repetir o título e sem aspas não escapadas.
- **Repo local em `~/MARCS_Blog`** (NUNCA /tmp — é apagado ao reiniciar). Fazer `git pull` antes de editar.

## Regras de estrutura e qualidade dos artigos
Estas regras são OBRIGATÓRIAS para qualquer artigo (gerado ou editado manualmente):

### Estrutura didática
1. **Introdução curta** que desperta interesse ("Imagina...", "Sentes que...") antes do primeiro heading.
2. **Passos numerados** ("Passo 1:", "Passo 2:", ...) para tutoriais práticos, cada um com: explicação + código + explicação do código.
3. **Conclusão** que resuma o que o leitor aprendeu + próximo passo sugerido.
4. **Artigo completo** — nunca deixar parágrafo, lista ou bloco de código cortado a meio.

### Qualidade de código
5. **Código funcional**: verificar mentalmente que executa (sintaxe, indentação, métodos definidos, imports). Nunca mostrar código que daria erro.
6. **Formato canónico de skill YAML** (usar SEMPRE):
   ```yaml
   name: <nome>
   description: <o que faz>
   author: MarcTechJA
   version: "1.0"
   inputs:
     <param>:
       type: string
       description: <para que serve>
       required: true
   steps:
     - name: <passo>
       action: <llm.generate|tools.file.read|tools.file.write|tools.shell.run|tools.email.send|tools.whatsapp.send|web_search>
       params:
         <chave>: "{{ inputs.<param> }}"
   outputs:
     <chave>: "<descrição do resultado>"
   ```
   - Referências: `{{ inputs.x }}` e `{{ steps.passo_anterior.output }}` (nunca `{x}`).
7. **Instalação**: macOS `brew install hermes-agent`; Linux/Windows → link para guia de instalação. Nunca `pip install hermes-agent`.
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

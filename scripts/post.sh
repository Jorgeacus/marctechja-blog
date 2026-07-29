#!/bin/bash
# =============================================================================
# MARC-Jarvis — Publicador Automático de Artigos
# =============================================================================
# Uso:
#   ./scripts/post.sh "Título do Artigo" "Categoria" "Autor" "Ficheiro com conteúdo HTML"
#
# Exemplo:
#   ./scripts/post.sh "Como Criar Skills" "Tutorial" "MARC-Jarvis" conteudo.html
#
# Se omitir o 4º argumento, lê o conteúdo da linha de comandos (stdin)
#
# Exemplo com stdin:
#   echo "<p>Conteúdo do artigo</p>" | ./scripts/post.sh "Meu Artigo" "IA"
# =============================================================================

set -e
export LC_ALL=en_US.UTF-8

# Cross-platform sed in-place
case "$(uname -s)" in
  Darwin*) sed_inplace() { sed -i '' "$@"; } ;;
  *)       sed_inplace() { sed -i "$@"; } ;;
esac

if [ $# -lt 1 ]; then
  echo "Erro: Indica pelo menos o título do artigo."
  echo "Uso: $0 \"Título\" [\"Categoria\"] [\"Autor\"] [\"Ficheiro\"]"
  exit 1
fi

TITLE="$1"
CATEGORY="${2:-Geral}"
AUTHOR="${3:-MARC-Jarvis}"
CONTENT_FILE="$4"
DATE=$(date +%d\ %b\ %Y)
SLUG=$(echo "$TITLE" \
  | tr '[:upper:]' '[:lower:]' \
  | sed -E 's/[àáâãäå]/a/g; s/[èéêë]/e/g; s/[ìíîï]/i/g; s/[òóôõö]/o/g; s/[ùúûü]/u/g; s/[ç]/c/g; s/[^a-z0-9]+/-/g; s/^-//; s/-$//')
POST_DIR="blog/$SLUG"

mkdir -p "$POST_DIR"

# Read content from file or stdin
if [ -n "$CONTENT_FILE" ]; then
  ARTICLE_CONTENT=$(cat "$CONTENT_FILE")
else
  ARTICLE_CONTENT=$(cat)
fi

# Default content if empty
if [ -z "$ARTICLE_CONTENT" ]; then
  ARTICLE_CONTENT="<p>Conteúdo do artigo em breve.</p>"
fi

# Generate SEO description (first 150 chars of content, strip HTML)
SEO_DESC=$(echo "$ARTICLE_CONTENT" \
  | sed 's/<[^>]*>//g; s/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g; s/&quot;/\"/g; s/&#39;/\x27/g' \
  | head -c 150 \
  | tr -d '\n' \
  | sed 's/[[:space:]]*$//')

cat > "$POST_DIR/index.html" << HTMLEOF
<!DOCTYPE html>
<html lang="pt-PT">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${TITLE} — MarctechJA</title>
  <meta name="description" content="${SEO_DESC}">
  <meta property="og:title" content="${TITLE}">
  <meta property="og:description" content="${SEO_DESC}">
  <meta property="og:url" content="https://marcusja777.com/${POST_DIR}/">
  <link rel="canonical" href="https://marcusja777.com/${POST_DIR}/">
  <link rel="stylesheet" href="/assets/css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⚡</text></svg>">
  <meta name="google-adsense-account" content="ca-pub-3717814491008089">
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="logo">Marc<span class="gold">tech</span>JA</a>
      <button class="menu-toggle" aria-label="Menu"><span></span><span></span><span></span></button>
      <ul class="nav-links">
        <li><a href="/">Home</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/livro/">Livro</a></li>
        <li><a href="/sobre/">Sobre</a></li>
      </ul>
    </div>
  </header>

  <section class="article-page">
    <div class="container layout-with-sidebar">
      <div>
        <div class="article-header">
          <div class="breadcrumb">
            <a href="/">Home</a> / <a href="/blog/">Blog</a> / ${TITLE}
          </div>
          <h1>${TITLE}</h1>
          <div class="meta">
            <span>📅 ${DATE}</span>
            <span>🏷️ ${CATEGORY}</span>
            <span>✍️ ${AUTHOR}</span>
          </div>
        </div>
        <div class="article-content">
          ${ARTICLE_CONTENT}

          <div class="article-cta">
            <h3>Queres ir mais longe?</h3>
            <p>O Guia Completo do Hermes Agent leva-te do zero às automações avançadas com 10 partes e 42 capítulos.</p>
            <a href="/livro/" class="btn btn-gold">Saber Mais Sobre o Livro</a>
          </div>
        </div>
      </div>
      <aside class="sidebar">
        <div class="sidebar-widget">
          <h3>📘 Livro do Hermes Agent</h3>
          <p>10 partes, 42 capítulos. PDF + EPUB.</p>
          <a href="/livro/" class="btn btn-gold">Saber Mais</a>
        </div>
        <div class="sidebar-widget ad-placeholder">Anúncio Google AdSense</div>
      </aside>
    </div>
  </section>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-inner">
        <div class="footer-brand">
          <a href="/" class="logo">Marc<span class="gold">tech</span>JA</a>
          <p>Tecnologia, automação e IA para transformar a produtividade.</p>
        </div>
        <div class="footer-col">
          <h4>Navegação</h4>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
            <li><a href="/livro/">Livro</a></li>
            <li><a href="/sobre/">Sobre</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Contacto</h4>
          <ul>
            <li><a href="mailto:marctechja@gmail.com">marctechja@gmail.com</a></li>
            <li><a href="https://github.com/Jorgeacus">GitHub</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 MarctechJA. Todos os direitos reservados.</p>
      </div>
    </div>
  </footer>
  <script src="/assets/js/main.js"></script>
</body>
</html>
HTMLEOF

# Add blog post to blog archive index
BLOG_ARCHIVE="blog/index.html"
if [ -f "$BLOG_ARCHIVE" ]; then
  EXCERPT=$(echo "$ARTICLE_CONTENT" | sed 's/<[^>]*>//g' | head -c 120 | tr -d '\n')
  NEW_CARD="            <article class=\"blog-card\">"
  NEW_CARD+="\n              <div class=\"blog-card-content\">"
  NEW_CARD+="\n                <div class=\"blog-card-tag\">${CATEGORY}</div>"
  NEW_CARD+="\n                <h2><a href=\"/${POST_DIR}/\">${TITLE}</a></h2>"
  NEW_CARD+="\n                <p>${EXCERPT}...</p>"
  NEW_CARD+="\n                <div class=\"meta\"><span class=\"date\">$(date +%d\ %b\ %Y)</span></div>"
  NEW_CARD+="\n              </div>"
  NEW_CARD+="\n            </article>"

  # Insert after first blog-grid div opening
  sed_inplace "s|<div class=\"blog-grid\">|<div class=\"blog-grid\">\n${NEW_CARD}|" "$BLOG_ARCHIVE"
fi

# Also update homepage
HOME_ARCHIVE="index.html"
if [ -f "$HOME_ARCHIVE" ]; then
  EXCERPT_HOME=$(echo "$ARTICLE_CONTENT" | sed 's/<[^>]*>//g' | head -c 100 | tr -d '\n')
  NEW_CARD_HOME="            <article class=\"blog-card\">"
  NEW_CARD_HOME+="\n              <div class=\"blog-card-content\">"
  NEW_CARD_HOME+="\n                <div class=\"blog-card-tag\">${CATEGORY}</div>"
  NEW_CARD_HOME+="\n                <h2><a href=\"/${POST_DIR}/\">${TITLE}</a></h2>"
  NEW_CARD_HOME+="\n                <p>${EXCERPT_HOME}...</p>"
  NEW_CARD_HOME+="\n                <div class=\"meta\"><span class=\"date\">$(date +%d\ %b\ %Y)</span> · novo</div>"
  NEW_CARD_HOME+="\n              </div>"
  NEW_CARD_HOME+="\n            </article>"

  sed_inplace "s|<div class=\"blog-grid\">|<div class=\"blog-grid\">\n${NEW_CARD_HOME}|" "$BLOG_ARCHIVE"
fi

# Auto-commit and push
cd "$(dirname "$0")/.."

# Configure git (works in both local and GitHub Actions)
git config user.name "MARC-Jarvis 🤖"
git config user.email "marctechja@gmail.com"

# Use GITHUB_TOKEN if in Actions, otherwise use default credentials
if [ -n "$GITHUB_TOKEN" ]; then
  git remote set-url origin "https://x-access-token:${GITHUB_TOKEN}@github.com/Jorgeacus/marctechja-blog.git"
fi

git add -A
git commit -m "Novo artigo: ${TITLE} [MARC-Jarvis]" 2>/dev/null || echo "Nada novo para commitar"
git push 2>/dev/null && echo "✅ Publicado!" || echo "⚠️ Falha no push. Faz git push manualmente."

echo ""
echo "📝 Artigo criado: ${POST_DIR}/"
echo "🔗 https://marcusja777.com/${POST_DIR}/"
echo ""

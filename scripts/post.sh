#!/bin/bash
# =============================================================================
# MARC-Jarvis Blog Post Script
# =============================================================================
# Uso:
#   ./scripts/post.sh "Título do Artigo" "Categoria" "Autor"
#
# Exemplo:
#   ./scripts/post.sh "Como Criar Skills no Hermes Agent" "Tutorial" "MARC-Jarvis"
#
# O script:
#   1. Cria pasta para o artigo com slug automático
#   2. Gera ficheiro index.html com metadados SEO
#   3. Abre o ficheiro no editor para colocares o conteúdo
#   4. Faz git add, commit e push
# =============================================================================

set -e

if [ $# -lt 1 ]; then
  echo "Erro: Indica pelo menos o título do artigo."
  echo "Uso: $0 \"Título do Artigo\" [\"Categoria\"] [\"Autor\"]"
  exit 1
fi

TITLE="$1"
CATEGORY="${2:-Geral}"
AUTHOR="${3:-MARC-Jarvis}"
DATE=$(date +%d\ %b\ %Y)
DATE_ISO=$(date +%Y-%m-%d)

# Generate URL-friendly slug
SLUG=$(echo "$TITLE" \
  | tr '[:upper:]' '[:lower:]' \
  | sed 's/[àáâãäå]/a/g; s/[èéêë]/e/g; s/[ìíîï]/i/g; s/[òóôõö]/o/g; s/[ùúûü]/u/g; s/[ç]/c/g; s/[^a-z0-9]+/-/g; s/^-//; s/-$//')

POST_DIR="blog/$SLUG"
mkdir -p "$POST_DIR"

cat > "$POST_DIR/index.html" << EOF
<!DOCTYPE html>
<html lang="pt-PT">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${TITLE} — MarctechJA</title>
  <meta name="description" content="ADICIONA UMA DESCRIÇÃO SEO AQUI">
  <meta property="og:title" content="${TITLE}">
  <meta property="og:description" content="ADICIONA UMA DESCRIÇÃO AQUI">
  <meta property="og:url" content="https://jorgeacus.github.io/marctechja-blog/${POST_DIR}/">
  <link rel="canonical" href="https://jorgeacus.github.io/marctechja-blog/${POST_DIR}/">
  <link rel="stylesheet" href="/marctechja-blog/assets/css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⚡</text></svg>">
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a href="/marctechja-blog/" class="logo">Marc<span class="gold">tech</span>JA</a>
      <button class="menu-toggle" aria-label="Menu"><span></span><span></span><span></span></button>
      <ul class="nav-links">
        <li><a href="/marctechja-blog/">Home</a></li>
        <li><a href="/marctechja-blog/blog/">Blog</a></li>
        <li><a href="/marctechja-blog/livro/">Livro</a></li>
        <li><a href="/marctechja-blog/sobre/">Sobre</a></li>
      </ul>
    </div>
  </header>

  <section class="article-page">
    <div class="container layout-with-sidebar">
      <div>
        <div class="article-header">
          <div class="breadcrumb">
            <a href="/marctechja-blog/">Home</a> / <a href="/marctechja-blog/blog/">Blog</a> / ${TITLE}
          </div>
          <h1>${TITLE}</h1>
          <div class="meta">
            <span>📅 ${DATE}</span>
            <span>🏷️ ${CATEGORY}</span>
            <span>✍️ ${AUTHOR}</span>
          </div>
        </div>
        <div class="article-content">
          <!-- ============================================ -->
          <!-- ESCREVE O CONTEÚDO DO ARTIGO AQUI EMBAIXO    -->
          <!-- ============================================ -->

          <p>Insere o teu conteúdo aqui...</p>

          <!-- ============================================ -->
          <!-- FIM DO CONTEÚDO                               -->
          <!-- ============================================ -->

          <div class="article-cta">
            <h3>Queres ir mais longe?</h3>
            <p>O Guia Completo do Hermes Agent leva-te do zero às automações avançadas com 10 partes e 42 capítulos.</p>
            <a href="/marctechja-blog/livro/" class="btn btn-gold">Saber Mais Sobre o Livro</a>
          </div>
        </div>
      </div>
      <aside class="sidebar">
        <div class="sidebar-widget">
          <h3>📘 Livro do Hermes Agent</h3>
          <p>10 partes, 42 capítulos. PDF + EPUB.</p>
          <a href="/marctechja-blog/livro/" class="btn btn-gold">Saber Mais</a>
        </div>
        <div class="sidebar-widget ad-placeholder">Anúncio Google AdSense</div>
      </aside>
    </div>
  </section>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-inner">
        <div class="footer-brand">
          <a href="/marctechja-blog/" class="logo">Marc<span class="gold">tech</span>JA</a>
          <p>Tecnologia, automação e IA para transformar a produtividade.</p>
        </div>
        <div class="footer-col">
          <h4>Navegação</h4>
          <ul>
            <li><a href="/marctechja-blog/">Home</a></li>
            <li><a href="/marctechja-blog/blog/">Blog</a></li>
            <li><a href="/marctechja-blog/livro/">Livro</a></li>
            <li><a href="/marctechja-blog/sobre/">Sobre</a></li>
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
  <script src="/marctechja-blog/assets/js/main.js"></script>
</body>
</html>
EOF

echo ""
echo "✅ Artigo criado: $POST_DIR/index.html"
echo ""
echo "Passos seguintes:"
echo "  1. Abre o ficheiro e substitui o conteúdo"
echo "  2. Executa: git add . && git commit -m \"Novo artigo: ${TITLE}\""
echo "  3. Executa: git push"
echo ""

#!/bin/bash
# =============================================================================
# Sincroniza o cache-busting do CSS (?v=YYYYMMDD) em TODAS as páginas HTML do
# site para a versão atual de assets/css/style.css.
#
# Versão derivada do último commit que tocou no style.css (data YYYYMMDD);
# fallback para a data de hoje. Idempotente — pode correr a qualquer momento.
# Usado pelo post.sh (a cada publicação) e pelo agente de manutenção.
# =============================================================================

set -e
export LC_ALL=en_US.UTF-8

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

case "$(uname -s)" in
  Darwin*) sed_inplace() { sed -i '' "$@"; } ;;
  *)       sed_inplace() { sed -i "$@"; } ;;
esac

CSS_VERSION="$(git -C "$REPO_ROOT" log -1 --format=%cs -- assets/css/style.css 2>/dev/null | tr -d '-')"
if [ -z "$CSS_VERSION" ]; then
  CSS_VERSION="$(date +%Y%m%d)"
fi

count=0
for f in $(grep -rl 'style\.css?v=' --include='*.html' "$REPO_ROOT" 2>/dev/null || true); do
  sed_inplace "s/style\.css?v=[0-9]*/style.css?v=${CSS_VERSION}/g" "$f"
  count=$((count + 1))
done

echo "↻ style.css?v=${CSS_VERSION} sincronizado em ${count} ficheiro(s)"

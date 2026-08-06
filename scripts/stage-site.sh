#!/bin/bash
# =============================================================================
# Prepara o diretório _site/ com APENAS os ficheiros do site (para deploy no
# Cloudflare Pages via `wrangler pages deploy _site`).
#
# O wrangler direct upload NÃO suporta exclusões (nem .assetsignore — isso é
# só Workers Assets) — carrega o diretório inteiro. Por isso preparamos um
# staging dir com rsync excluindo ficheiros de desenvolvimento.
# =============================================================================

set -e
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STAGE="$REPO_ROOT/_site"

rm -rf "$STAGE"
mkdir -p "$STAGE"

rsync -a --delete \
  --exclude='.git' \
  --exclude='.github' \
  --exclude='.hermes' \
  --exclude='.gitignore' \
  --exclude='AGENTS.md' \
  --exclude='scripts' \
  --exclude='node_modules' \
  --exclude='_site' \
  --exclude='subscribers.csv' \
  "$REPO_ROOT/" "$STAGE/"

count=$(find "$STAGE" -type f | wc -l | tr -d ' ')
echo "→ _site pronto: ${count} ficheiro(s) (em $STAGE)"

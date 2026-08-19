#!/usr/bin/env python3
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parent.parent / "blog"
# Artigos onde o CTA do corpo é parte essencial do propósito (lançamento do ebook)
KEEP = {"hermes-agent-book-launch"}

def fix_article(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    orig = html

    # Remove o bloco <div class="article-cta">...</div> no fim do corpo
    html, n = re.subn(
        r'\n\s*<div class="article-cta">.*?</div>\s*(?=</div>\s*</div>\s*<aside)',
        '',
        html,
        count=1,
        flags=re.DOTALL,
    )
    if n:
        path.write_text(html, encoding="utf-8")
        print(f"REMOVED CTA {path.relative_to(BLOG.parent)}")
        return True
    print(f"SKIP {path.relative_to(BLOG.parent)} (sem bloco removível)")
    return False

def main() -> None:
    changed = 0
    for article in sorted(BLOG.iterdir()):
        if article.name in KEEP:
            continue
        f = article / "index.html"
        if f.exists() and fix_article(f):
            changed += 1
    print(f"Total ficheiros alterados: {changed}")

if __name__ == "__main__":
    main()
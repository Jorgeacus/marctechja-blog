#!/usr/bin/env python3
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parent.parent / "blog"

COMMENTS_BLOCK = """<div class="comments-section">
          <h2>Comentários</h2>
          <script src="https://giscus.app/client.js"
                  data-repo="Jorgeacus/marctechja-blog"
                  data-repo-id="R_kgDOTnRVjw"
                  data-category="General"
                  data-category-id="DIC_kwDOTnRVj84DDt4R"
                  data-mapping="pathname"
                  data-strict="0"
                  data-reactions-enabled="1"
                  data-emit-metadata="0"
                  data-input-position="bottom"
                  data-theme="preferred_color_scheme"
                  data-lang="pt"
                  crossorigin="anonymous"
                  async>
          </script>
          <noscript>Ativa o JavaScript para veres e deixares comentários.</noscript>
        </div>"""

def fix_article(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    if "giscus" in html:
        print(f"SKIP {path.relative_to(BLOG.parent)} (já tem giscus)")
        return False
    # Insere a secção de comentários entre o fecho do article-content e o aside
    new_html, n = re.subn(
        r'(\n      </div>\n      <aside)',
        '\n' + COMMENTS_BLOCK + r'\1',
        html,
        count=1,
    )
    if n:
        path.write_text(new_html, encoding="utf-8")
        print(f"ADDED {path.relative_to(BLOG.parent)}")
        return True
    print(f"WARN {path.relative_to(BLOG.parent)}: padrão de inserção não encontrado")
    return False

def main() -> None:
    changed = 0
    for article in sorted(BLOG.iterdir()):
        f = article / "index.html"
        if f.exists() and fix_article(f):
            changed += 1
    print(f"Total ficheiros alterados: {changed}")

if __name__ == "__main__":
    main()
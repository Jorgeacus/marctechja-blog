#!/usr/bin/env python3
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parent.parent / "blog"
# O artigo de lançamento é o propósito do CTA; manter hotm.io direto
KEEP_HOTM = {"hermes-agent-book-launch"}
# O artigo de afiliados contém exemplo de HTML escapado (&lt;a href="https://hotm.io...)
# O regex só captura tags <a> reais, por isso o exemplo escapado não é afetado.

def fix_article(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    orig = html

    html = re.sub(
        r'(<a[^>]*href=")https://hotm\.io/jFUussV9(")',
        r'\1/livro/\2',
        html,
    )

    if html != orig:
        path.write_text(html, encoding="utf-8")
        print(f"CONVERTED {path.relative_to(BLOG.parent)}")
        return True
    print(f"SKIP {path.relative_to(BLOG.parent)} (sem links hotm.io)")
    return False

def main() -> None:
    changed = 0
    for article in sorted(BLOG.iterdir()):
        if article.name in KEEP_HOTM:
            continue
        f = article / "index.html"
        if f.exists() and fix_article(f):
            changed += 1
    print(f"Total ficheiros alterados: {changed}")

if __name__ == "__main__":
    main()
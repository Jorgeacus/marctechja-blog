#!/usr/bin/env python3
import re
import sys
from pathlib import Path

BLOG = Path(__file__).resolve().parent.parent / "blog"
AUTHOR = "Marcus"
AUTHOR_URL = "https://github.com/Jorgeacus"
OLD_META = 'content="Hermes Agent"'
NEW_META = f'content="{AUTHOR}"'

def fix_article(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    orig = html

    html = html.replace('>✍️ Hermes Agent<', f'>✍️ {AUTHOR}<')

    html = html.replace(
        f'<meta name="author" {OLD_META}>',
        f'<meta name="author" {NEW_META}>',
    )

    html = re.sub(
        r'<meta name="author" content="Hermes Agent">',
        f'<meta name="author" content="{AUTHOR}">',
        html,
    )

    html = re.sub(
        r'"author": \{"@type": "Person", "name": "Hermes Agent"\}',
        f'"author": {{"@type": "Person", "name": "{AUTHOR}", "url": "{AUTHOR_URL}"}}',
        html,
    )

    html = re.sub(
        r'"author": \{\s*"@type": "Person",\s*"name": "Hermes Agent"\s*\}',
        f'"author": {{\n    "@type": "Person",\n    "name": "{AUTHOR}",\n    "url": "{AUTHOR_URL}"\n  }}',
        html,
    )

    if html != orig:
        path.write_text(html, encoding="utf-8")
        return True
    return False

def main() -> None:
    changed = 0
    for article in sorted(BLOG.iterdir()):
        f = article / "index.html"
        if f.exists():
            if fix_article(f):
                changed += 1
                print(f"FIXED {f.relative_to(BLOG.parent)}")
    print(f"Total ficheiros alterados: {changed}")

if __name__ == "__main__":
    main()
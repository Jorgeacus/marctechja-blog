#!/usr/bin/env python3
import re
import html as htmlmod
from pathlib import Path

BLOG = Path(__file__).resolve().parent.parent / "blog"
WPM = 200

def real_words(article_html: str) -> int:
    m = re.search(r'<div class="article-content">(.*?)</div>\s*</div>\s*</div>\s*<aside', article_html, re.DOTALL)
    body = m.group(1) if m else article_html
    text = re.sub(r'<[^>]+>', ' ', body)
    text = htmlmod.unescape(text)
    return len(re.findall(r'\S+', text))

def fix_article(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    words = real_words(html)
    if words < 30:
        return False
    minutes = max(1, round(words / WPM))
    orig = html

    if re.search(r'min de leitura', html):
        html = re.sub(
            r'\d+ min de leitura',
            f'{minutes} min de leitura',
            html,
            count=1,
        )
        print(f"FIXED {path.relative_to(BLOG.parent)} ({words} palavras -> {minutes} min, já tinha marcador)")
    else:
        # Adiciona o marcador de leitura após o span da data
        html = re.sub(
            r'(<div class="meta">\s*<span>📅 [^<]*</span>)',
            rf'\1\n            <span>📖 {minutes} min de leitura</span>',
            html,
            count=1,
        )
        print(f"FIXED {path.relative_to(BLOG.parent)} ({words} palavras -> {minutes} min, marcador adicionado)")

    if html != orig:
        path.write_text(html, encoding="utf-8")
        return True
    print(f"SKIP  {path.relative_to(BLOG.parent)} (sem alteração)")
    return False

def main() -> None:
    changed = 0
    for article in sorted(BLOG.iterdir()):
        f = article / "index.html"
        if f.exists():
            if fix_article(f):
                changed += 1
    print(f"Total ficheiros alterados: {changed}")

if __name__ == "__main__":
    main()
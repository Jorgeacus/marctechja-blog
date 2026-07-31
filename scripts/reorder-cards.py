#!/usr/bin/env python3
"""
Reordena os cards do blog archive e da homepage dentro do primeiro <div class="blog-grid">,
do mais recente para o mais antigo (por data visível no card).

Uso:
  python3 scripts/reorder-cards.py [ficheiro1 ficheiro2 ...]
  # sem argumentos, processa blog/index.html e index.html por omissão
"""

import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TARGETS = [REPO_ROOT / "blog" / "index.html"]

DATE_RE = re.compile(r'class="date">([^<]+)<')
CARD_RE = re.compile(r'(<article class="blog-card">.*?</article>)', re.DOTALL)


def parse_date(datestr):
    text = datestr.strip().replace("· novo", "").strip()
    try:
        return datetime.strptime(text, "%d %b %Y")
    except Exception:
        return datetime(1900, 1, 1)


def reorder_file(path):
    path = Path(path)
    if not path.exists():
        print(f"  ⚠️ {path} não existe — a saltar")
        return 0
    content = path.read_text(encoding="utf-8")

    marker = '<div class="blog-grid">'
    start = content.find(marker)
    if start == -1:
        print(f"  ⚠️ {path}: sem blog-grid — a saltar")
        return 0

    # Find the matching closing </div> for the grid (first one after the grid's own </div>s).
    # Cards are the only direct children; we search for the end of the grid by scanning
    # for the first '</div>' that closes the grid after the last card.
    grid_start = start + len(marker)
    grid_end = content.find("</div>", grid_start)
    # The grid content contains nested divs; find the true grid end by matching the last
    # card's closing </article> followed by whitespace/newline + </div>
    last_card_end = content.rfind("</article>", grid_start)
    if last_card_end == -1:
        print(f"  ⚠️ {path}: sem cards no grid — a saltar")
        return 0
    grid_end = content.find("</div>", last_card_end)

    grid_content = content[grid_start:grid_end]
    cards = CARD_RE.findall(grid_content)
    if not cards:
        print(f"  ⚠️ {path}: sem cards extraídos")
        return 0

    # Preserve the indentation of the first card
    indent = ""
    m = re.match(r"\s*", grid_content)
    if m:
        indent = m.group(0)

    dated = []
    undated = []
    for card in cards:
        dm = DATE_RE.search(card)
        if dm:
            dated.append((parse_date(dm.group(1)), card))
        else:
            undated.append(card)

    dated.sort(key=lambda x: x[0], reverse=True)
    sorted_cards = [c for _, c in dated] + undated

    separator = "\n\n"
    new_grid_content = indent + separator.join(sorted_cards).replace(
        "\n" + indent, "\n" + indent
    ) + "\n"

    new_content = content[:grid_start] + new_grid_content + content[grid_end:]
    path.write_text(new_content, encoding="utf-8")
    print(f"  ✅ {path}: {len(sorted_cards)} cards reordenados (recente → antigo)")
    return len(sorted_cards)


def main():
    targets = [Path(t) for t in sys.argv[1:]] if len(sys.argv) > 1 else DEFAULT_TARGETS
    total = 0
    for t in targets:
        total += reorder_file(t)
    if total == 0:
        print("Nenhum card reordenado.")
        sys.exit(1)
    print(f"Done: {total} cards no total.")


if __name__ == "__main__":
    main()

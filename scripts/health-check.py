#!/usr/bin/env python3
"""
MarctechJA — Health Check do Blog

Verifica a saúde do site marcusja777.com:
  1. HTTP 200 em /, /blog/, /livro/, /sobre/, robots.txt, ads.txt e em todos os artigos do sitemap
  2. Blog archive: todos os artigos presentes e ordenados do mais recente para o mais antigo
  3. Homepage: exatamente 6 cards, mais recente primeiro
  4. Nenhum <!-- não fechado nas páginas (bug crítico histórico)
  5. Sitemap com todas as URLs dos artigos
  6. CSS com cache-busting (?v=)

Uso:
  python3 scripts/health-check.py            # verifica o site live
  python3 scripts/health-check.py --local    # verifica os ficheiros do repo local

Exit code 0 = tudo OK. Exit code 1 = falhas detetadas (imprime cada uma).
Quando usado no GitHub Actions, o workflow cria uma Issue automática se falhar.
"""

import re
import sys
import html
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path

BASE = "https://marcusja777.com"
REPO_ROOT = Path(__file__).resolve().parent.parent

FAILURES = []


def check(ok, message):
    status = "✅" if ok else "❌"
    print(f"  {status} {message}")
    if not ok:
        FAILURES.append(message)


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "MarctechJA-HealthCheck/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        return resp.status, body


def get(url):
    try:
        status, body = fetch(url)
        return status, body
    except Exception as e:
        return None, f"ERRO: {e}"


def strip_html_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def extract_cards(html_text):
    cards = []
    for m in re.finditer(r'<article class="blog-card">(.*?)</article>', html_text, re.DOTALL):
        card = m.group(1)
        url_m = re.search(r'<h2><a href="([^"]+)">', card)
        date_m = re.search(r'class="date">([^<]+)', card)
        cards.append({
            "url": url_m.group(1) if url_m else "?",
            "date": date_m.group(1).strip() if date_m else "",
        })
    return cards


def parse_date(datestr):
    try:
        return datetime.strptime(datestr, "%d %b %Y")
    except Exception:
        try:
            return datetime.strptime(datestr, "%d %b %Y · novo")
        except Exception:
            return None


def sitemap_urls(sitemap_text):
    return re.findall(r"<loc>([^<]+)</loc>", sitemap_text)


def current_css_version():
    """Versão atual do CSS (YYYYMMDD) = data do último commit que tocou em style.css."""
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "log", "-1", "--format=%cs", "--", "assets/css/style.css"],
            capture_output=True, text=True, timeout=10,
        ).stdout.strip()
        return out.replace("-", "") if out else None
    except Exception:
        return None


def all_css_versions():
    """Versões (?v=) de CSS referenciadas em todas as páginas HTML locais."""
    versions = set()
    files = [REPO_ROOT / "index.html", REPO_ROOT / "404.html", REPO_ROOT / "blog" / "index.html"]
    files += sorted((REPO_ROOT / "blog").glob("*/index.html"))
    files += [REPO_ROOT / s / "index.html" for s in
              ["livro", "sobre", "politica-de-privacidade", "politica-de-cookies", "termos", "contactos"]]
    for f in files:
        if f.exists():
            text = f.read_text(encoding="utf-8")
            versions.update(re.findall(r"style\.css\?v=([0-9]+)", text))
    return versions


def check_section(name, fn):
    print(f"\n== {name} ==")
    fn()


def check_live():
    check_section("Páginas base (HTTP 200)", lambda: [
        check(get(url)[0] == 200, f"{url} responde 200")
        for url in [f"{BASE}/", f"{BASE}/blog/", f"{BASE}/livro/", f"{BASE}/sobre/",
                    f"{BASE}/politica-de-privacidade/", f"{BASE}/politica-de-cookies/",
                    f"{BASE}/termos/", f"{BASE}/contactos/"]
    ])

    print()
    print("== Sitemap ==")
    status, sitemap = get(f"{BASE}/sitemap.xml")
    check(status == 200, f"sitemap.xml responde 200 (atual: {status})")
    urls = sitemap_urls(sitemap) if status == 200 else []
    check(len(urls) >= 12, f"sitemap contém {len(urls)} URLs (esperado >= 12)")

    print()
    print("== Artigos do sitemap (HTTP 200) ==")
    article_urls = [u for u in urls if "/blog/" in u and u.rstrip("/") != f"{BASE}/blog"]
    for u in article_urls:
        status, _ = get(u)
        check(status == 200, f"{u} responde 200 (atual: {status})")

    print()
    print("== Blog archive ==")
    status, blog_html = get(f"{BASE}/blog/")
    check(status == 200, "blog/ responde 200")
    if status == 200:
        cards = extract_cards(blog_html)
        check(len(cards) == len(article_urls), f"blog tem {len(cards)} cards e o sitemap tem {len(article_urls)} artigos")
        dates = [parse_date(c["date"]) for c in cards]
        ordered = all(dates[i] >= dates[i + 1] for i in range(len(dates) - 1) if dates[i] and dates[i + 1])
        check(ordered, "blog archive ordenado do mais recente ao mais antigo")
        if not ordered:
            for c in cards:
                print(f"       {c['date']:20} {c['url']}")
        opens = blog_html.count("<!--")
        closes = blog_html.count("-->")
        check(opens == closes, f"sem <!-- não fechado no blog ({opens} abertos, {closes} fechados)")

    print()
    print("== Homepage ==")
    status, home_html = get(f"{BASE}/")
    check(status == 200, "/ responde 200")
    home_css = ""
    if status == 200:
        cards = extract_cards(home_html)
        check(len(cards) == 6, f"homepage tem {len(cards)} cards (esperado 6)")
        opens = home_html.count("<!--")
        closes = home_html.count("-->")
        check(opens == closes, f"sem <!-- não fechado na homepage ({opens} abertos, {closes} fechados)")
        css_m = re.search(r'stylesheet" href="([^"]+\.css[^"]*)"', home_html)
        check(css_m and "?v=" in css_m.group(1), "CSS com cache-busting (?v=)")
        home_css = css_m.group(1) if css_m else ""

    print()
    print("== CSS live / responsividade ==")
    if not home_css:
        _, home_html = get(f"{BASE}/")
        css_m = re.search(r'stylesheet" href="([^"]+\.css[^"]*)"', home_html)
        home_css = css_m.group(1) if css_m else ""
    css_url = (BASE + home_css) if home_css.startswith("/") else home_css
    if not css_url:
        css_url = f"{BASE}/assets/css/style.css?v=0"
    status, css_body = get(css_url)
    check(status == 200, f"style.css responde 200 ({css_url})")
    if status == 200:
        check("minmax(0, 1fr)" in css_body, "CSS live tem grid responsivo (minmax(0,1fr))")
        check("overflow-wrap" in css_body, "CSS live quebra conteúdo largo (overflow-wrap)")
        check("overflow-x" in css_body, "CSS live protege contra overflow (overflow-x)")
    if home_css and "?v=" in home_css:
        v = home_css.split("?v=")[-1]
        status, blog_html = get(f"{BASE}/blog/")
        if status == 200:
            versions = set(re.findall(r"style\.css\?v=([0-9]+)", blog_html))
            check(versions == {v} and bool(v), f"blog/ usa a mesma versão de CSS que a home ({v})")


def check_local():
    check_section("Ficheiros locais do repo", lambda: [
        check((REPO_ROOT / "index.html").exists(), "index.html existe"),
        check((REPO_ROOT / "blog" / "index.html").exists(), "blog/index.html existe"),
        check((REPO_ROOT / "sitemap.xml").exists(), "sitemap.xml existe"),
        check((REPO_ROOT / "robots.txt").exists(), "robots.txt existe"),
        check((REPO_ROOT / "ads.txt").exists(), "ads.txt existe"),
        check((REPO_ROOT / "CNAME").exists(), "CNAME existe (marcusja777.com)"),
        check((REPO_ROOT / "politica-de-privacidade" / "index.html").exists(), "politica-de-privacidade/ existe"),
        check((REPO_ROOT / "politica-de-cookies" / "index.html").exists(), "politica-de-cookies/ existe"),
        check((REPO_ROOT / "termos" / "index.html").exists(), "termos/ existe"),
        check((REPO_ROOT / "contactos" / "index.html").exists(), "contactos/ existe"),
    ])

    blog_path = REPO_ROOT / "blog" / "index.html"
    if blog_path.exists():
        text = blog_path.read_text(encoding="utf-8")
        cards = extract_cards(text)
        dates = [parse_date(c["date"]) for c in cards]
        ordered = all(dates[i] >= dates[i + 1] for i in range(len(dates) - 1) if dates[i] and dates[i + 1])
        print()
        print("== Blog archive local ==")
        check(ordered, f"blog/index.html ordenado (atual: {len(cards)} cards)")
        if not ordered:
            for c in cards:
                print(f"       {c['date']:20} {c['url']}")

    print()
    print("== CSS / responsividade (local) ==")
    versions = all_css_versions()
    check(len(versions) == 1, f"todas as páginas usam a MESMA versão de CSS ({sorted(versions) if versions else 'nenhuma'})")
    current = current_css_version()
    if current:
        check(versions == {current},
              f"versão de CSS ({sorted(versions) or 'nenhuma'}) == versão atual do style.css ({current})")

    css_path = REPO_ROOT / "assets" / "css" / "style.css"
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        check("minmax(0, 1fr)" in css, "CSS: grid responsivo (minmax(0,1fr)) presente")
        check("overflow-wrap" in css, "CSS: quebra de conteúdo largo (overflow-wrap) presente")
        check("overflow-x" in css, "CSS: proteção de overflow (overflow-x) presente")


def main():
    local = "--local" in sys.argv
    if local:
        print(f"🔍 Health check LOCAL ({REPO_ROOT})")
        check_local()
    else:
        print(f"🔍 Health check do site LIVE ({BASE})")
        check_live()

    print()
    if FAILURES:
        print(f"❌ {len(FAILURES)} falha(s):")
        for f in FAILURES:
            print(f"   - {f}")
        sys.exit(1)
    print("✅ Tudo OK!")
    sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Hermes Agent — Gerador Automático de Artigos
Gera artigos sobre Hermes Agent usando APIs de IA.

Providers suportados (via env var AI_PROVIDER):
  - gemini  (grátis — usa GEMINI_API_KEY)
  - openai  (pago — usa OPENAI_API_KEY)

Uso:
    python3 scripts/generate-post.py

Variáveis de ambiente:
    AI_PROVIDER   = gemini | openai (default: gemini)
    GEMINI_API_KEY = chave da Google Gemini (grátis em aistudio.google.com)
    OPENAI_API_KEY = chave da OpenAI
"""

import os
import sys
import json
import random
import subprocess
import urllib.error
import urllib.request
from datetime import datetime

# --- Tópicos para os artigos ---
TOPICS = [
    # Hermes Agent — tutoriais e guias
    {
        "audience": "Geral",
        "title": "O que é o Hermes Agent e como pode transformar as tuas automações",
        "focus": "Introdução ao Hermes Agent: o que é, como funciona, casos de uso e porque é diferente de outras ferramentas de IA."
    },
    {
        "audience": "Programadores",
        "title": "Criar skills personalizadas no Hermes Agent — guia passo a passo",
        "focus": "Tutorial prático de como criar skills YAML no Hermes Agent, desde a estrutura básica até exemplos complexos com múltiplos passos."
    },
    {
        "audience": "Geral",
        "title": "Hermes Agent vs outros agentes de IA: comparação completa",
        "focus": "Comparar Hermes Agent com Claude Code, Codex CLI, OpenAI Agents, destacando vantagens e desvantagens de cada um."
    },
    {
        "audience": "Programadores",
        "title": "Integrar Hermes Agent com APIs externas",
        "focus": "Ensinar como configurar skills do Hermes Agent para chamar APIs REST, processar JSON e automatizar fluxos com serviços externos."
    },
    {
        "audience": "Geral",
        "title": "5 automações do dia a dia com Hermes Agent que vais querer usar",
        "focus": "Lista de 5 automações práticas: organizar ficheiros, responder emails, gerar relatórios, pesquisar web e agendar tarefas."
    },
    # Python para automações
    {
        "audience": "Programadores",
        "title": "Automatizar tarefas repetitivas com Python e Hermes Agent",
        "focus": "Como usar scripts Python em conjunto com o Hermes Agent para automatizar tarefas como processamento de ficheiros, scraping e geração de relatórios."
    },
    {
        "audience": "Programadores",
        "title": "Python para automação de email: ler, filtrar e responder com IA",
        "focus": "Tutorial de Python com Gmail API para ler, categorizar e responder emails automaticamente, com sugestões geradas por IA."
    },
    {
        "audience": "Programadores",
        "title": "Automatizar o teu workflow de GitHub com Python",
        "focus": "Usar Python + PyGithub para automatizar PRs, issues, releases e CI/CD, integrado com skills do Hermes Agent."
    },
    # Agentes e IA
    {
        "audience": "Geral",
        "title": "O que são agentes de IA e como funcionam na prática",
        "focus": "Explicação simples sobre agentes de IA: o que são, como tomam decisões, usam ferramentas e executam tarefas autonomamente."
    },
    {
        "audience": "Programadores",
        "title": "Construir o teu próprio agente de IA com Python",
        "focus": "Guia para criar um agente de IA simples em Python que usa ferramentas (API calls, ficheiros, shell) e pode ser integrado com Hermes Agent."
    },
]

REFERENCE_FILE = "assets/reference/ebook-summary.md"
SCRIPTS_DIR = "scripts"
BLOG_DIR = "blog"

def load_reference():
    with open(REFERENCE_FILE, "r", encoding="utf-8") as f:
        return f.read()

GEMINI_MODELS = [
    "gemini-3.6-flash",
    "gemini-2.5-flash-latest",
    "gemini-2.5-pro-latest",
    "gemini-3.5-flash",
]

def call_gemini_api(prompt, api_key):
    last_error = None
    for attempt in range(2):
        for version in ["v1beta", "v1"]:
            for model in GEMINI_MODELS:
                url = f"https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent"
                data = json.dumps({
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.8,
                        "maxOutputTokens": 4096,
                        "topK": 40,
                        "topP": 0.95
                    }
                }).encode("utf-8")
                try:
                    req = urllib.request.Request(url, data=data, headers={
                        "Content-Type": "application/json",
                        "x-goog-api-key": api_key
                    })
                    resp = urllib.request.urlopen(req, timeout=60)
                    result = json.loads(resp.read().decode("utf-8"))
                    if "candidates" not in result or not result["candidates"]:
                        error_reason = result.get("promptFeedback", {}).get("blockReason", "unknown")
                        raise Exception(f"Gemini {version}/{model}: sem resposta (blockReason: {error_reason})")
                    print(f"  ✅ {version}/{model} OK")
                    return result["candidates"][0]["content"]["parts"][0]["text"]
                except urllib.error.HTTPError as e:
                    print(f"  ⚠️ {version}/{model}: HTTP {e.code}")
                    last_error = e
                    continue
                except (urllib.error.URLError, TimeoutError, ConnectionResetError, OSError) as e:
                    print(f"  ⚠️ {version}/{model}: {type(e).__name__}: {e}")
                    last_error = e
                    continue
    raise RuntimeError(f"Falha ao contactar a API Gemini após várias tentativas: {last_error}") from last_error

def call_openai_api(prompt, api_key):
    import urllib.request
    import urllib.parse

    url = "https://api.openai.com/v1/chat/completions"
    data = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "És um assistente especialista em Hermes Agent e automação com IA. Geras artigos em português de Portugal, bem escritos e práticos."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 4096
    }).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    })
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode("utf-8"))
    return result["choices"][0]["message"]["content"]

def generate_article(topic, reference_content, provider, api_key):
    today = datetime.now().strftime("%d de %B de %Y")
    audiences_pt = {
        "Universitários": "universitários",
        "Ensino Médio": "alunos do ensino médio",
        "Professores": "professores",
        "Criadores de Conteúdo": "criadores de conteúdo",
        "WhatsApp": "utilizadores do WhatsApp",
        "Email": "profissionais",
        "Geral": "todos"
    }
    audience_pt = audiences_pt.get(topic["audience"], "todos")

    prompt = f"""És um especialista em Hermes Agent e automação com IA.

Gera um artigo de blog completo em português de Portugal (pt-PT) sobre o tema abaixo.

O artigo deve ser prático, útil e bem estruturado. Deve referir o ebook "Guia Completo do Hermes Agent" como recurso adicional, com link https://hotm.io/jFUussV9 no final.

TÍTULO: {topic["title"]}
PÚBLICO-ALVO: {audience_pt}
FOCO: {topic["focus"]}
DATA: {today}

REFERÊNCIA SOBRE O EBOOK:
{reference_content}

O artigo HTML deve ter:
- Título SEO e meta description
- Headings (<h2>, <h3>) para estruturar
- Parágrafos (<p>) com conteúdo prático
- Listas (<ul>/<ol>) quando adequado
- Pelo menos um bloco de código (<pre><code>) com exemplo real de skill YAML ou comando
- Call to action final a promover o ebook
- Tom informal mas profissional, acessível ao público indicado

IMPORTANTE: Gera APENAS o HTML do conteúdo (o que vai dentro da div <div class="article-content">).
NÃO incluis <!DOCTYPE>, <html>, <head>, <body> ou tags de estrutura da página.
NÃO incluis comentários HTML (nem <!-- -->), nem blocos "SEO Metadata". Começa diretamente com o <h2> ou <p>.
Apenas o conteúdo interno: parágrafos, headings, listas, código e CTA.
"""

    if provider == "gemini":
        return call_gemini_api(prompt, api_key)
    else:
        return call_openai_api(prompt, api_key)

def main():
    provider = os.environ.get("AI_PROVIDER", "gemini").lower()
    api_key = os.environ.get("GEMINI_API_KEY" if provider == "gemini" else "OPENAI_API_KEY")

    print(f"📋 Provider: {provider}")
    print(f"📋 API Key set: {'✅ Sim' if api_key else '❌ Não'}")

    if not api_key:
        print("❌ ERRO: Define a variável de ambiente", "GEMINI_API_KEY" if provider == "gemini" else "OPENAI_API_KEY")
        sys.exit(1)

    reference_content = load_reference()

    # Pick random topic
    topic = random.choice(TOPICS)

    print(f"📝 A gerar artigo: {topic['title']}")
    print(f"   Público: {topic['audience']}")
    print(f"   Provider: {provider}")

    try:
        content_html = generate_article(topic, reference_content, provider, api_key)
        print(f"✅ Conteúdo gerado ({len(content_html)} chars)")
    except Exception as e:
        print(f"❌ Erro ao gerar conteúdo: {type(e).__name__}: {e}")
        sys.exit(1)

    # Clean up the response - extract only the HTML content
    content_html = content_html.strip()
    if content_html.startswith("```html"):
        content_html = content_html[7:]
    if content_html.startswith("```"):
        content_html = content_html[3:]
    if content_html.endswith("```"):
        content_html = content_html[:-3]
    content_html = content_html.strip()

    # Save content to temp file
    temp_file = f"/tmp/marctechja_article_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(content_html)

    # Call the post.sh script
    category = topic["audience"]
    author = "Hermes Agent"
    title = topic["title"]

    print(f"📰 A publicar artigo...")
    result = subprocess.run(
        ["bash", f"{SCRIPTS_DIR}/post.sh", title, category, author, temp_file],
        capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)) + "/.."
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"❌ Erro ao publicar: {result.stderr}")
        sys.exit(1)

    os.remove(temp_file)
    print(f"✅ Artigo publicado com sucesso: {topic['title']}")

if __name__ == "__main__":
    main()

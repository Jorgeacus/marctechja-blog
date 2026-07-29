#!/usr/bin/env python3
"""
MARC-Jarvis — Gerador Automático de Artigos
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
from datetime import datetime

# --- Tópicos para os artigos ---
TOPICS = [
    {
        "audience": "Universitários",
        "title": "Como usar o Hermes Agent para criar resumos de artigos científicos",
        "focus": "Explicar como estudantes universitários podem usar o Hermes Agent para ler PDFs de artigos, extrair pontos principais, gerar resumos e criar fichas de estudo automaticamente."
    },
    {
        "audience": "Ensino Médio",
        "title": "Cria o teu primeiro assistente de estudo com Hermes Agent",
        "focus": "Tutorial simples para alunos do ensino médio criarem um assistente que tira dúvidas de matemática, ciências e história usando o Hermes Agent."
    },
    {
        "audience": "Professores",
        "title": "Automatizar a correção de trabalhos com Hermes Agent",
        "focus": "Como professores podem usar skills do Hermes Agent para corrigir redações, dar feedback personalizado e acompanhar o progresso dos alunos."
    },
    {
        "audience": "Criadores de Conteúdo",
        "title": "Agenda e publica nas redes sociais com Hermes Agent",
        "focus": "Automatizar a criação e agendamento de posts para Instagram, YouTube e Telegram usando skills do Hermes Agent."
    },
    {
        "audience": "WhatsApp",
        "title": "Cria um assistente de WhatsApp com Hermes Agent",
        "focus": "Como configurar o Hermes Agent para responder automaticamente a mensagens no WhatsApp, agendar lembretes e enviar respostas inteligentes."
    },
    {
        "audience": "Email",
        "title": "Ler e responder emails automaticamente com Hermes Agent",
        "focus": "Automatizar a gestão de email: ler, categorizar, responder e arquivar mensagens usando skills do Hermes Agent."
    },
    {
        "audience": "Universitários",
        "title": "Hermes Agent para programar trabalhos em grupo",
        "focus": "Como equipas de estudantes podem usar o Hermes Agent para organizar tarefas, gerir prazos e colaborar em projetos académicos."
    },
    {
        "audience": "Criadores de Conteúdo",
        "title": "Gerar legendas e descrições para YouTube com IA",
        "focus": "Usar o Hermes Agent para gerar títulos, descrições SEO, tags e legendas para vídeos do YouTube automaticamente."
    },
    {
        "audience": "Professores",
        "title": "Criar planos de aula com Hermes Agent em segundos",
        "focus": "Como professores podem usar o Hermes Agent para gerar planos de aula completos, com objetivos, atividades e avaliações."
    },
    {
        "audience": "Geral",
        "title": "5 automações que todo estudante devia conhecer no Hermes Agent",
        "focus": "Lista de 5 automações práticas para estudantes: resumos, pesquisa, organização, lembretes e tradução."
    },
]

REFERENCE_FILE = "assets/reference/ebook-summary.md"
SCRIPTS_DIR = "scripts"
BLOG_DIR = "blog"

def load_reference():
    with open(REFERENCE_FILE, "r", encoding="utf-8") as f:
        return f.read()

def call_gemini_api(prompt, api_key):
    import urllib.request
    import urllib.parse

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    data = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 4096,
            "topK": 40,
            "topP": 0.95
        }
    }).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode("utf-8"))
    return result["candidates"][0]["content"]["parts"][0]["text"]

def call_openai_api(prompt, api_key):
    import urllib.request
    import urllib.parse

    url = "https://api.openai.com/v1/chat/completions"
    data = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "És o MARC-Jarvis, um assistente especialista em Hermes Agent e automação com IA. Geras artigos em português de Portugal, bem escritos e práticos."},
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

    prompt = f"""És o MARC-Jarvis, especialista em Hermes Agent e automação com IA.

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
    author = "MARC-Jarvis 🤖"
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

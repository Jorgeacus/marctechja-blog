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
import subprocess
import urllib.error
import urllib.request
from datetime import datetime

# --- Tópicos para os artigos ---
# Ordenados do mais simples/rápido de automatizar para o mais complexo.
# A rotação é sequencial (1 tema por dia, por ordem) — ver main().
# NOTA: não repetir temas/artigos já publicados; só atualizar ou aprofundar.
TOPICS = [
    # 1 — WhatsApp: mensagens (o mais simples de começar)
    {
        "audience": "Geral",
        "title": "Automatizar mensagens no WhatsApp com Hermes Agent",
        "focus": "Guia simples para configurar o Hermes Agent e automatizar o envio de mensagens no WhatsApp: respostas automáticas, lembretes e mensagens agendadas."
    },
    # 2 — Criação de sites: landing page simples
    {
        "audience": "Criadores de Conteúdo",
        "title": "Criar uma landing page simples com HTML e CSS em 30 minutos",
        "focus": "Tutorial passo a passo para criar uma landing page básica em HTML e CSS, pronta para publicar, sem precisar de programação avançada."
    },
    # 3 — Python para automação: começar
    {
        "audience": "Programadores",
        "title": "Python para automação: por onde começar",
        "focus": "Guia de introdução à automação com Python: instalar, primeiros scripts, bibliotecas essenciais (os, requests, schedule) e exemplos simples."
    },
    # 4 — Telegram
    {
        "audience": "Geral",
        "title": "Automatizar o Telegram com Hermes Agent: respostas e agendamentos",
        "focus": "Como automatizar um grupo ou canal no Telegram com o Hermes Agent: responder a mensagens, publicar atualizações e agendar posts."
    },
    # 5 — Empresas: WhatsApp Business (novo, fácil)
    {
        "audience": "Empresas",
        "title": "Automatizar o atendimento no WhatsApp Business com Hermes Agent",
        "focus": "Como micro e grandes empresas podem automatizar respostas a clientes no WhatsApp Business: mensagens de boas-vindas, FAQs, lembretes e catálogo, usando o Hermes Agent."
    },
    # 6 — Landing page para produto
    {
        "audience": "Criadores de Conteúdo",
        "title": "Criar uma landing page para o teu produto com HTML e CSS",
        "focus": "Como estruturar uma landing page de produto: título, benefícios, prova social, chamada para ação e formulário de captura, com HTML e CSS."
    },
    # 7 — WhatsApp: áudio e imagens
    {
        "audience": "Geral",
        "title": "Enviar áudio e imagens automáticos no WhatsApp com Hermes Agent",
        "focus": "Automatizar o envio de mensagens de áudio (geradas por IA) e imagens no WhatsApp com o Hermes Agent: casos práticos e configuração."
    },
    # 8 — Combinação Python + Hermes Agent
    {
        "audience": "Programadores",
        "title": "Automatizar tarefas repetitivas com Python e Hermes Agent",
        "focus": "Como usar scripts Python em conjunto com o Hermes Agent para automatizar tarefas como processamento de ficheiros, scraping e geração de relatórios."
    },
    # 9 — Instagram
    {
        "audience": "Criadores de Conteúdo",
        "title": "Automatizar o Instagram com Hermes Agent: agendar e publicar",
        "focus": "Planeamento e publicação automática de conteúdo no Instagram com o Hermes Agent: ideias de posts, legendas, hashtags e agendamento."
    },
    # 10 — Landing page para afiliados
    {
        "audience": "Afiliados",
        "title": "Landing pages para afiliados: estrutura que converte",
        "focus": "Como criar landing pages de afiliados com HTML e CSS: secções que convertem, links de afiliado, prova social e chamada para ação eficaz."
    },
    # 11 — Empresas: análise de mercado
    {
        "audience": "Empresários",
        "title": "Análise de mercado com Hermes Agent: relatórios automáticos",
        "focus": "Como empresários de micro e grandes empresas podem usar o Hermes Agent para gerar relatórios de análise de mercado: concorrentes, tendências, preços e oportunidades, recolhendo dados da web automaticamente."
    },
    # 12 — Criação de sites com Python
    {
        "audience": "Programadores",
        "title": "Criar um site com Python e publicar de graça",
        "focus": "Como construir um site simples em Python (Flask ou páginas estáticas) e publicá-lo gratuitamente em plataformas como GitHub Pages."
    },
    # 13 — Empresas: análise de produtos (lojas online e físicas)
    {
        "audience": "Empresas",
        "title": "Análise de produtos com Hermes Agent para lojas online e físicas",
        "focus": "Como lojas online e físicas, de micro a grandes empresas, podem usar o Hermes Agent para analisar produtos: acompanhar preços, stock, reviews e concorrência, e gerar relatórios de desempenho automaticamente."
    },
    # 14 — Python para email
    {
        "audience": "Programadores",
        "title": "Python para automação de email: ler, filtrar e responder com IA",
        "focus": "Tutorial de Python com Gmail API para ler, categorizar e responder emails automaticamente, com sugestões geradas por IA."
    },
    # 15 — Empresas: landing pages para captar clientes
    {
        "audience": "Empresários",
        "title": "Landing pages para captar clientes: guia para empresários",
        "focus": "Como empresários de micro e grandes empresas podem criar landing pages eficazes para captar clientes: oferta, benefícios, prova social, formulário e chamada para ação, com HTML e CSS simples."
    },
    # 16 — Empresas: gestão de tráfego (orgânico e pago)
    {
        "audience": "Empresários",
        "title": "Gestão de tráfego orgânico e pago para empreendedores com Hermes Agent",
        "focus": "Como empreendedores de micro e grandes empresas podem usar o Hermes Agent para gerir tráfego: planear SEO e conteúdo orgânico, acompanhar campanhas pagas, monitorizar anúncios e gerar relatórios de desempenho automaticamente."
    },
    # 17 — Hermes Agent: APIs externas
    {
        "audience": "Programadores",
        "title": "Integrar Hermes Agent com APIs externas",
        "focus": "Ensinar como configurar skills do Hermes Agent para chamar APIs REST, processar JSON e automatizar fluxos com serviços externos."
    },
    # 18 — Empresas: Instagram para negócios
    {
        "audience": "Empresas",
        "title": "Automatizar o Instagram de uma empresa com Hermes Agent",
        "focus": "Como micro e grandes empresas podem automatizar a presença no Instagram: agendar posts de produtos, gerar legendas e hashtags e responder a mensagens, tudo com o Hermes Agent."
    },
    # 19 — GitHub com Python
    {
        "audience": "Programadores",
        "title": "Automatizar o teu workflow de GitHub com Python",
        "focus": "Usar Python + PyGithub para automatizar PRs, issues, releases e CI/CD, integrado com skills do Hermes Agent."
    },
    # 20 — Empresas: gestão de redes sociais
    {
        "audience": "Empresários",
        "title": "Gestão de redes sociais para empreendedores com Hermes Agent",
        "focus": "Como empreendedores de micro e grandes empresas podem usar o Hermes Agent para gerir as redes sociais: planear calendários de conteúdo, gerar posts e legendas, agendar publicações e analisar resultados em várias plataformas automaticamente."
    },
    # 21 — Empresas: Telegram para empresas
    {
        "audience": "Empresas",
        "title": "Automatizar o Telegram de uma empresa com Hermes Agent",
        "focus": "Como micro e grandes empresas podem usar o Hermes Agent para automatizar canais e grupos no Telegram: comunicados, novidades, atendimento e integrações internas."
    },
    # 22 — Comparação de agentes
    {
        "audience": "Geral",
        "title": "Hermes Agent vs outros agentes de IA: comparação completa",
        "focus": "Comparar Hermes Agent com Claude Code, Codex CLI, OpenAI Agents, destacando vantagens e desvantagens de cada um."
    },
    # 22 — Construir o próprio agente com Python
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

def validate_content(html_content, title):
    """Valida a qualidade do HTML gerado antes de publicar.

    Deteta artigos truncados (a meio de parágrafo/código), tags partidas,
    comentários HTML no corpo, <h1> duplicado e outros problemas estruturais.
    Devolve lista de erros (vazia = válido).
    """
    import re

    errors = []

    # 1. Tags <pre><code> balanceadas (blocos de código fechados)
    open_pre = html_content.count("<pre>")
    close_pre = html_content.count("</pre>")
    if open_pre != close_pre:
        errors.append(f"{open_pre} <pre> abertos mas {close_pre} fechados — bloco de código cortado")

    # 2. Comentários HTML (são removidos na publicação e quebram validação)
    if "<!--" in html_content:
        errors.append("comentário HTML (<!--) no corpo do artigo")

    # 3. <h1> no corpo (título já aparece no topo — duplica no excerpt/cards)
    if "<h1>" in html_content:
        errors.append("<h1> no corpo do artigo (não usar; headings internos começam em <h2>)")

    # 4. Título repetido como primeiro heading do corpo
    first_h2 = re.search(r"<h2[^>]*>(.*?)</h2>", html_content, re.S)
    if first_h2:
        import html as h
        heading_text = h.unescape(re.sub(r"<[^>]+>", "", first_h2.group(1))).strip().lower()
        clean_title = title.lower().strip()
        if clean_title in heading_text:
            errors.append("primeiro <h2> repete o título do artigo")

    # 5. Parágrafo/heading cortado a meio (bloco HTML sem tag de fecho no fim do texto)
    if html_content.rstrip().endswith(("</p>", "</h2>", "</h3>", "</li>", "</pre>", "</ul>", "</ol>", "</div>")):
        pass  # termina bem
    else:
        errors.append("conteúdo parece cortado a meio (não termina numa tag de fecho válida)")

    # 6. Limite mínimo de conteúdo (artigo sem corpo útil)
    text_len = len(re.sub(r"<[^>]+>", "", html_content).strip())
    if text_len < 400:
        errors.append(f"corpo demasiado curto ({text_len} caracteres de texto)")

    return errors


def generate_article(topic, reference_content, provider, api_key):
    today = datetime.now().strftime("%d de %B de %Y")
    audiences_pt = {
        "Universitários": "universitários",
        "Ensino Médio": "alunos do ensino médio",
        "Professores": "professores",
        "Criadores de Conteúdo": "criadores de conteúdo",
        "WhatsApp": "utilizadores do WhatsApp",
        "Email": "profissionais",
        "Afiliados": "afiliados e criadores de ofertas",
        "Empresas": "micro e grandes empresas e lojas",
        "Empresários": "empresários e donos de negócio de micro e grandes empresas",
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

REGRAS DE QUALIDADE OBRIGATÓRIAS:

1. ESTRUTURA DIDÁTICA:
   - Começa com um parágrafo de introdução curto que desperta interesse (ex: "Imagina...", "Sentes que...") antes do primeiro heading.
   - Usa passos numerados ("Passo 1:", "Passo 2:", ...) para tutoriais práticos.
   - Cada passo tem: explicação breve + bloco de código + explicação do que o código faz.
   - Termina com uma conclusão que resuma o que o leitor aprendeu e o próximo passo sugerido.
   - NUNCA deixes um parágrafo ou código cortado a meio — o artigo tem de estar completo do início ao fim.
   - NUNCA comeces um bloco de código e o deixes sem terminar (cada <pre><code> ... </code></pre> tem de estar fechado).

2. REGRAS DE CÓDIGO (funcionalidade e consistência):
   - Os blocos de código têm de ser COMPLETOS e COERENTES — verifica mentalmente que funcionam antes de os escreveres (sintaxe, indentação, nomes, chaves, parênteses).
   - Usa SEMPRE o formato canónico de skill YAML do Hermes Agent com esta estrutura exata:
     name: <nome>
     description: <o que faz>
     author: MarcTechJA
     version: "1.0"
     inputs:
        <param>: {{ type: string, description: <para que serve>, required: true }}
     steps:
       - name: <passo>
         action: <llm.generate | tools.file.read | tools.file.write | tools.shell.run | tools.email.send | tools.whatsapp.send | web_search>
         params:
           <chave>: "{{ inputs.<param> }}"   (ou "{{ steps.<passo_anterior>.output }}")
     outputs:
       <chave>: "<descrição do resultado>"
   - Usa sempre "inputs:" (NUNCA "parameters:") e referências "{{ inputs.x }}" / "{{ steps.x.output }}" (NUNCA "{{x}}").
   - Em código Python: não uses métodos que não estejam definidos; todo o código apresentado tem de executar sem erro.
   - Não inventes URLs de repositórios (usa apenas https://github.com/HermesAgent/hermes-agent.git, https://python.org, https://git-scm.com, https://ollama.ai/install.sh).
   - Comando de instalação consistente: macOS "brew install hermes-agent"; Linux/Windows remetem para o guia de instalação. NUNCA "pip install hermes-agent".

3. REGRAS DE LIMPEZA:
   - NÃO incluis comentários HTML (nem <!-- -->) no corpo — são removidos na publicação e quebram a validação.
   - NÃO incluis <h1> no corpo (o título já aparece no topo da página) — os headings internos começam em <h2>.
   - NÃO repitas o título como primeiro heading ou como meta description (evita duplicação no excerpt e nos cards).
   - Meta description completa, com pontuação final e sem cortes a meio.

IMPORTANTE: Gera APENAS o HTML do conteúdo (o que vai dentro da div <div class="article-content">).
NÃO incluis <!DOCTYPE>, <html>, <head>, <body> ou tags de estrutura da página.
NÃO incluis comentários HTML (nem <!-- -->), nem blocos "SEO Metadata". Começa diretamente com o <h2> ou <p>.
NÃO repitas o título como primeiro heading do corpo (o título já é mostrado no topo da página) — começa diretamente com o primeiro tópico.
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

    # Pick today's topic: sequential rotation, one per day, starting with the simplest.
    # Uses a stable index so each calendar day maps to one topic (dois dias = dois temas).
    today_index = (datetime.now() - datetime(2026, 8, 1)).days
    topic = TOPICS[today_index % len(TOPICS)]

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

    # --- Validação de qualidade pós-geração ---
    errors = validate_content(content_html, topic["title"])
    if errors:
        print("❌ Artigo rejeitado — problema(s) de qualidade:")
        for e in errors:
            print(f"   - {e}")
        print("   A gerar novamente...")
        try:
            content_html = generate_article(topic, reference_content, provider, api_key)
            content_html = content_html.strip()
            if content_html.startswith("```html"):
                content_html = content_html[7:]
            if content_html.startswith("```"):
                content_html = content_html[3:]
            if content_html.endswith("```"):
                content_html = content_html[:-3]
            content_html = content_html.strip()
            errors = validate_content(content_html, topic["title"])
            if errors:
                print("❌ Segunda tentativa também falhou:")
                for e in errors:
                    print(f"   - {e}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Erro na segunda tentativa: {e}")
            sys.exit(1)

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

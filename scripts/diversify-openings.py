#!/usr/bin/env python3
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parent.parent / "blog"

# Novo parágrafo de abertura COMPLETO (corpo) para cada artigo
NEW_BODY = {
    "analise-de-mercado-com-hermes-agent-relatorios-automaticos":
        "Monitorizar a concorrência e acompanhar os preços em tempo real é uma corrida contra o tempo para qualquer negócio — seja uma pequena loja local ou uma grande empresa. A recolha manual de dados da web consome centenas de horas que poderiam ser investidas em decisões estratégicas. A boa notícia é que o Hermes Agent permite automatizar todo este processo, gerando relatórios de análise de mercado completos e atualizados em questão de minutos.",
    "analise-de-produtos-com-hermes-agent-para-lojas-online-e-fisicas":
        "Verificar manualmente os preços da concorrência, checar o stock disponível e ler avaliações de clientes são tarefas que ocupam horas preciosas do dia de qualquer lojista. Quer gerencies uma pequena loja física de bairro ou uma grande plataforma de e-commerce, acompanhar o ritmo alucinante do mercado retalhista é um desafio constante. A boa notícia é que podes automatizar toda esta operação de recolha e análise de produtos utilizando o Hermes Agent.",
    "automatizar-o-atendimento-no-whatsapp-business-com-hermes-agent":
        "No mercado atual, a rapidez na resposta é o fator decisivo entre fechar um negócio ou perder o cliente para a concorrência. Para uma pequena loja de bairro ou uma grande empresa, responder a tempo a todas as mensagens no WhatsApp Business nem sempre é possível, e cada atraso pode significar uma venda perdida. A boa notícia é que podes automatizar todo este processo — desde saudações iniciais e respostas a dúvidas frequentes até ao envio de catálogos e lembretes — de forma inteligente com o Hermes Agent.",
    "automatizar-o-instagram-com-hermes-agent-agendar-e-publicar":
        "Legendas, hashtags, agendamentos e interação com o público — manter a consistência numa rede social exige disciplina diária. Muitos criadores gastam mais tempo a planear publicações do que a produzir conteúdo relevante, e é aqui que a automação faz a diferença. Com a ajuda do Hermes Agent, podes transformar essa rotina cansativa num fluxo estruturado e automatizado.",
    "automatizar-o-instagram-de-uma-empresa-com-hermes-agent":
        "Planear o calendário editorial, escrever legendas criativas, pesquisar hashtags relevantes e responder a dezenas de mensagens diretas (DMs) — gerir o Instagram da tua empresa pode parecer um trabalho a tempo inteiro. Felizmente, com o avanço da Inteligência Artificial, já podes automatizar grande parte deste processo. O Hermes Agent é uma ferramenta de IA open-source que te permite criar agentes autónomos para gerir a presença digital da tua marca de forma eficiente, personalizada e totalmente automatizada.",
    "automatizar-o-telegram-com-hermes-agent-respostas-e-agendamentos":
        "Responder às mesmas perguntas no teu grupo do Telegram e manter o teu canal atualizado com conteúdos regulares exige consistência, mas consumir todo o teu tempo útil é um custo demasiado alto. Gerir uma comunidade pede dedicação diária, e responder manualmente a cada mensagem e agendar atualizações pode esgotar qualquer equipa. A boa notícia é que podes automatizar estas tarefas de forma simples e inteligente utilizando o Hermes Agent.",
    "automatizar-o-telegram-de-uma-empresa-com-hermes-agent":
        "Copiar e colar novidades, responder às mesmas perguntas dos clientes ou partilhar relatórios internos de forma manual são tarefas que consomem horas preciosas da tua equipa. Gerir a comunicação de uma empresa ou de uma loja digital exige agilidade, e cada minuto gasto em trabalho repetitivo é tempo que falta para decisões importantes. É aqui que entra o Hermes Agent, um assistente de Inteligência Artificial open-source concebido para correr localmente ou na cloud e automatizar fluxos de trabalho complexos de forma extremamente simples.",
    "automatizar-o-teu-workflow-de-github-com-python":
        "Rever Pull Requests pendentes, categorizar issues ou preparar notas de lançamento para novos releases são tarefas repetitivas que ocupam tempo valioso no GitHub. A combinação da linguagem Python com a biblioteca PyGithub e a capacidade autónoma do Hermes Agent permite transformar o teu fluxo de trabalho diário numa máquina de produtividade automatizada.",
    "automatizar-tarefas-repetitivas-com-python-e-hermes-agent":
        "Ler ficheiros CSV, fazer scraping de dados na Web ou formatar relatórios semanais são apenas alguns exemplos de tarefas repetitivas que consomem horas do teu dia. A boa notícia é que podes automatizar todo esse trabalho manual combinando a flexibilidade da linguagem Python com o poder de orquestração do Hermes Agent.",
    "construir-o-teu-proprio-agente-de-ia-com-python":
        "Os chatbots tradicionais limitam-se a conversar — não conseguem realizar ações reais no teu computador. Imagina ter um assistente inteligente que não só compreende as tuas instruções, mas que também executa scripts em Python, manipula ficheiros locais e interage com APIs externas de forma totalmente autónoma. Criar o teu próprio agente de IA é muito mais simples do que parece, especialmente quando combinamos a flexibilidade de programação do Python com o ecossistema do Hermes Agent.",
    "criar-uma-landing-page-para-o-teu-produto-com-html-e-css":
        "Produzir conteúdos incríveis é apenas metade do trabalho: na hora de lançar um e-book, curso ou comunidade, a criação da página de vendas torna-se muitas vezes o principal bloqueio. Ter uma estrutura simples, rápida e que converta visitantes em subscritores ou clientes não precisa de exigir plataformas pagas e complexas. Com o conhecimento certo de HTML e CSS — e o apoio da automação —, podes construir a tua própria landing page personalizada em questão de minutos.",
    "gestao-de-trafego-organico-e-pago-para-empreendedores-com-hermes-agent":
        "A gestão de tráfego orgânico e pago divide a atenção de qualquer empresário entre a criação de conteúdo e a análise interminável de métricas de anúncios. Gerir o crescimento de um negócio exige visão estratégica, mas tarefas repetitivas como pesquisar palavras-chave SEO, acompanhar o ROI de campanhas no Google e Meta Ads ou compilar relatórios semanais acabam por sobrecarregar qualquer equipa. O Hermes Agent surge como uma plataforma de automação com Inteligência Artificial capaz de transformar o teu terminal num centro de comando de marketing digital totalmente automatizado.",
    "hermes-agent-vs-outros-agentes-de-ia-comparacao-completa":
        "O ecossistema de inteligência artificial move-se a uma velocidade estonteante, e escolher a ferramenta certa para automatizar o teu dia a dia tornou-se uma decisão estratégica. Imagina poderes executar tarefas complexas diretamente no teu terminal, alternando entre modelos de IA na cloud e modelos 100% locais que protegem a privacidade dos teus dados. Em 2026, a escolha do agente de IA ideal tornou-se uma decisão estratégica para programadores, empreendedores e criadores de conteúdo.",
    "integrar-hermes-agent-com-apis-externas":
        "Uma inteligência artificial isolada do resto do mundo digital tem o seu valor limitado. Imagina dar ao teu assistente a capacidade de consultar o tempo em tempo real, verificar a cotação de moedas, atualizar o teu CRM ou disparar notificações para um canal do Slack. Tudo isto é possível quando integramos o Hermes Agent com APIs REST externas.",
    "landing-pages-para-afiliados-estrutura-que-converte":
        "Enviar centenas de visitantes para as tuas ofertas de afiliados e ver poucos deles converterem é um dos problemas mais frustrantes do marketing digital. A chave para transformar cliques em comissões reais reside na estrutura da tua landing page. Quando aliamos a simplicidade do HTML e CSS à potência de automação com IA do Hermes Agent, torna-se possível criar e testar páginas de alta conversão em poucos minutos.",
    "landing-pages-para-captar-clientes-guia-para-empresarios":
        "Receber visitantes no site todos os dias não garante novos contactos ou reuniões agendadas no fim do mês. Para empresários e donos de negócios — quer gerenciem uma microempresa local ou uma grande organização —, o segredo do crescimento sustentável não está apenas em atrair tráfego, mas sim em converter esse tráfego em clientes potenciais (leads). É exatamente para isto que serve uma landing page eficaz.",
    "python-para-automacao-de-email-ler-filtrar-e-responder-com-ia":
        "A caixa de entrada do Gmail pode ser um autêntico sorvedouro de produtividade, consumindo metade do teu dia de trabalho em leitura, organização e respostas que poderiam ser geridas de forma automática. Felizmente, combinando o poder do Python com a inteligência artificial do Hermes Agent, podemos criar um sistema autónomo que lê a tua caixa de entrada, categoriza os emails importantes e rascunha respostas inteligentes de forma imediata.",
    "python-para-automacao-por-onde-comecar":
        "Organizar pastas, descarregar ficheiros ou copiar dados de um lado para o outro são tarefas que ocupam horas do teu dia — e que o computador podia fazer sozinho. A boa notícia é que podes colocar o teu computador a trabalhar por ti. O Python é a linguagem ideal para dar os primeiros passos no mundo da automação, permitindo transformar processos manuais demorados em scripts simples que correm em segundos.",
    "seo-para-o-teu-blog-ou-site-com-python-e-hermes-agent":
        "Analisar palavras-chave, redigir meta descriptions e tentar perceber porque é que os teus artigos não alcançam as primeiras posições do Google são tarefas que consomem horas preciosas a qualquer criador de conteúdo. Otimizar o teu site para motores de pesquisa (SEO) é essencial para atrair tráfego orgânico qualificado, mas pode tornar-se extremamente repetitivo. A boa notícia é que podes automatizar grande parte deste processo combinando a flexibilidade do Python com a inteligência do Hermes Agent. Neste guia prático, vais aprender a criar rotinas automatizadas para auditorias de palavras-chave, otimização de títulos e metadados, análise de backlinks e geração de relatórios de desempenho.",
}

def fix_article(path: Path, new_body: str) -> bool:
    html = path.read_text(encoding="utf-8")
    orig = html

    # 1. Substituir o primeiro parágrafo do corpo
    m = re.search(r'(<div class="article-content">\s*<p>)(.*?)(</p>)', html, re.DOTALL)
    if not m:
        print(f"WARN {path.relative_to(BLOG.parent)}: corpo não encontrado")
        return False
    html = html[:m.start(2)] + new_body + html[m.end(2):]

    # 2. Corrigir meta description e og:description que começam com "Sentes que"
    def fix_meta(md: str) -> str:
        if md.startswith("Sentes que"):
            return new_body
        return md
    html = re.sub(
        r'(<meta name="description" content=")([^"]*)(")',
        lambda m: m.group(1) + fix_meta(m.group(2)) + m.group(3),
        html,
    )
    html = re.sub(
        r'(<meta property="og:description" content=")([^"]*)(")',
        lambda m: m.group(1) + fix_meta(m.group(2)) + m.group(3),
        html,
    )

    if html != orig:
        path.write_text(html, encoding="utf-8")
        print(f"FIXED {path.relative_to(BLOG.parent)}")
        return True
    print(f"NOCHANGE {path.relative_to(BLOG.parent)}")
    return False

def main() -> None:
    changed = 0
    for article, new_body in NEW_BODY.items():
        f = BLOG / article / "index.html"
        if f.exists() and fix_article(f, new_body):
            changed += 1
    print(f"Total ficheiros alterados: {changed}")

if __name__ == "__main__":
    main()
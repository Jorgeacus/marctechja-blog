#!/usr/bin/env python3
# =============================================================================
# Agente de manutenção automática (sub-agente de classificação)
# -----------------------------------------------------------------------------
# Recebe o log de um workflow do GitHub Actions que falhou e devolve UMA ação
# de manutenção, escolhida por um modelo de IA com um CONJUNTO DE AÇÕES
# FECHADO. O resultado sai no stdout em duas linhas:
#
#   ACTION=<regenerate|sync_css|nothing|issue>
#   DIAG=<diagnóstico em texto livre>
#
# Qualquer falha (sem chave, API indisponível, resposta inválida, ação fora do
# conjunto) cai para ACTION=issue — abrir Issue para humano. NUNCA age fora
# do conjunto permitido.
# =============================================================================

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

ALLOWED = {"regenerate", "sync_css", "nothing", "issue"}

SYSTEM = """És o agente de manutenção do blog MarctechJA (marcusja777.com, repo Jorgeacus/marctechja-blog).

Um workflow do GitHub Actions falhou. Recebes o log e contexto. Devolve EXATAMENTE um objeto JSON, sem mais texto, sem explicações, sem repetir instruções:

{"action": "<uma de: regenerate|sync_css|nothing|issue>", "reason": "<explicação breve>"}

Escolhe a ação:
- regenerate: o artigo diário NÃO foi publicado; falha na geração/validação/truncamento ou falha recuperável da API.
- sync_css: inconsistência da versão de CSS (?v=) entre páginas.
- nothing: falha transitória de infraestrutura (timeout, 5xx) sem impacto no conteúdo.
- issue: erro de lógica, estrutura, design, HTML quebrado ou situação ambígua — abre Issue para humano.

NUNCA inventes outras ações. Se o log não for conclusivo, escolhe issue. Não uses "regenerate" se o log mostrar que o artigo já foi publicado."""


def git_context(repo_root):
    try:
        log = subprocess.run(
            ["git", "-C", repo_root, "log", "--oneline", "-12", "--date=short", "--pretty=%h %ad %s"],
            capture_output=True, text=True, timeout=15,
        )
        return log.stdout.strip()[:2000]
    except Exception:
        return ""


def call_gemini(prompt, key):
    models = ["gemini-3.6-flash", "gemini-3.5-flash"]
    last = None
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        data = json.dumps({
            "contents": [{"role": "user", "parts": [{"text": SYSTEM + "\n\n--- LOG DO RUN FALHADO ---\n" + prompt}]}],
            "generationConfig": {"temperature": 0.1, "maxOutputTokens": 1200},
        }).encode()
        try:
            r = urllib.request.Request(url, data=data, headers={
                "Content-Type": "application/json",
                "x-goog-api-key": key,
            })
            resp = urllib.request.urlopen(r, timeout=45)
            res = json.loads(resp.read().decode())
            return res["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            last = e
    raise RuntimeError(f"Gemini indisponível: {last}")


def main():
    log_path = sys.argv[1] if len(sys.argv) > 1 else ""
    repo_root = sys.argv[2] if len(sys.argv) > 2 else ""

    if not log_path or not os.path.exists(log_path):
        print("ACTION=issue")
        print("DIAG=Sem log do run falhado para classificar.")
        return 0

    try:
        with open(log_path, "r", encoding="utf-8", errors="replace") as f:
            log = f.read()
    except Exception as e:
        print("ACTION=issue")
        print(f"DIAG=Não foi possível ler o log: {e}")
        return 0

    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        print("ACTION=issue")
        print("DIAG=Sem GEMINI_API_KEY no workflow de manutenção para classificar a falha.")
        return 0

    ctx = git_context(repo_root)
    tail = log[-7000:]
    prompt = f"TREINO: devolve JSON.\n\nDATA DE HOJE: {os.popen('date -u +%Y-%m-%d').read().strip()}\n\nÚLTIMOS COMMITS:\n{ctx}\n\n--- LOG (últimos 7000 chars) ---\n{tail}"

    try:
        text = call_gemini(prompt, key)
    except Exception as e:
        print("ACTION=issue")
        print(f"DIAG=Erro ao contactar a IA de diagnóstico: {e}")
        return 0

    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        obj = None
        if start != -1 and end > 0:
            try:
                obj = json.loads(text[start:end])
            except Exception:
                obj = None
        if obj is None:
            import re
            m = re.search(r'"action"\s*:\s*"([a-z_]+)"', text)
            if not m:
                raise ValueError("sem action")
            obj = {"action": m.group(1), "reason": text[:400]}
        action = obj.get("action", "")
        reason = str(obj.get("reason", ""))
    except Exception:
        print("ACTION=issue")
        print(f"DIAG=Resposta da IA não foi JSON válido: {text[:300]!r}")
        return 0

    if action not in ALLOWED:
        print("ACTION=issue")
        print(f"DIAG=Ação inválida devolvida pela IA: {action!r} — a falha foi reencaminhada para humano.")
        return 0

    print(f"ACTION={action}")
    print(f"DIAG={reason[:500]}".replace("\n", " "))
    return 0


if __name__ == "__main__":
    sys.exit(main())

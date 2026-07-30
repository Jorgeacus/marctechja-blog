#!/usr/bin/env python3
"""
MARC-Jarvis — Gmail Monitor & Assistant
Ler, pesquisar, responder a emails via Gmail API.

Uso:
    python3 scripts/gmail_monitor.py auth                               # primeira autenticação
    python3 scripts/gmail_monitor.py search --query "convite especial"
    python3 scripts/gmail_monitor.py read --id <msg_id>
    python3 scripts/gmail_monitor.py reply --id <msg_id> --body "..."   # cria draft + mostra
    python3 scripts/gmail_monitor.py send --to "x@y" --subject "..." --body "..."
    python3 scripts/gmail_monitor.py unread

Variáveis de ambiente (automação):
    GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REFRESH_TOKEN
"""

import os, sys, json, base64, argparse
from datetime import datetime, timedelta
from email.mime.text import MIMEText

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
]
TOKEN_FILE = os.path.expanduser("~/.marcjarvis_gmail_token.json")
CREDENTIALS_FILE = os.path.expanduser("~/.marcjarvis_gmail_credentials.json")


def get_credentials():
    client_id = os.environ.get("GMAIL_CLIENT_ID")
    client_secret = os.environ.get("GMAIL_CLIENT_SECRET")
    refresh_token = os.environ.get("GMAIL_REFRESH_TOKEN")
    if client_id and client_secret and refresh_token:
        return {"client_id": client_id, "client_secret": client_secret, "refresh_token": refresh_token}
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return json.load(f)
    return None


def get_service():
    creds = get_credentials()
    if not creds:
        print("❌ Sem credenciais. Executa: python3 scripts/gmail_monitor.py auth")
        sys.exit(1)
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
    except ImportError:
        print("❌ Instala: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        sys.exit(1)
    creds_obj = Credentials(
        token=None, refresh_token=creds["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=creds["client_id"], client_secret=creds["client_secret"],
        scopes=SCOPES,
    )
    return build("gmail", "v1", credentials=creds_obj)


def search_messages(service, query, max_results=20):
    messages, page_token = [], None
    while len(messages) < max_results:
        resp = service.users().messages().list(
            userId="me", q=query, pageToken=page_token, maxResults=min(50, max_results)
        ).execute()
        batch = resp.get("messages", [])
        messages.extend(batch)
        page_token = resp.get("nextPageToken")
        if not page_token or not batch:
            break
    return messages[:max_results]


def get_message_details(service, msg_id):
    msg = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
    snippet = msg.get("snippet", "")
    body = ""
    parts = msg["payload"].get("parts", [])
    if not parts and "body" in msg["payload"] and "data" in msg["payload"]["body"]:
        parts = [msg["payload"]]
    for part in parts:
        if part.get("mimeType") == "text/plain" and "data" in part.get("body", {}):
            body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="replace")
            break
        for sub in part.get("parts", []):
            if sub.get("mimeType") == "text/plain" and "data" in sub.get("body", {}):
                body = base64.urlsafe_b64decode(sub["body"]["data"]).decode("utf-8", errors="replace")
                break
        if body:
            break
    return {
        "id": msg_id,
        "thread_id": msg["threadId"],
        "subject": headers.get("Subject", "(sem assunto)"),
        "from": headers.get("From", ""),
        "to": headers.get("To", ""),
        "date": headers.get("Date", ""),
        "snippet": snippet,
        "body": body,
    }


def create_draft(service, to, subject, body, thread_id=None, msg_id=None):
    message = MIMEText(body, _charset="utf-8")
    message["To"] = to
    message["Subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    draft_body = {"message": {"raw": raw}}
    if thread_id:
        draft_body["message"]["threadId"] = thread_id
    draft = service.users().drafts().create(userId="me", body=draft_body).execute()
    return draft


def send_message(service, to, subject, body, thread_id=None):
    message = MIMEText(body, _charset="utf-8")
    message["To"] = to
    message["Subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    body = {"raw": raw}
    if thread_id:
        body["threadId"] = thread_id
    sent = service.users().messages().send(userId="me", body=body).execute()
    return sent


def send_draft(service, draft_id):
    sent = service.users().drafts().send(userId="me", id=draft_id).execute()
    return sent


def mark_as_read(service, msg_id):
    service.users().messages().modify(
        userId="me", id=msg_id, body={"removeLabelIds": ["UNREAD"]}
    ).execute()


# --- Comandos ---

def cmd_auth(args):
    from google_auth_oauthlib.flow import InstalledAppFlow
    path = args.credentials or CREDENTIALS_FILE
    if not os.path.exists(path):
        print(f"❌ Credenciais não encontradas: {path}")
        print("1. https://console.cloud.google.com/apis/credentials")
        print("2. Criar 'OAuth 2.0 Client ID' → Desktop app")
        print("3. Download JSON →", path)
        sys.exit(1)
    print("⚠️  Antes de continuar, certifica-te que já adicionaste o teu email")
    print("   como 'Test user' em https://console.cloud.google.com/apis/credentials/consent")
    print("   Se não, faz isso primeiro e depois volta aqui.\n")
    input("Prima Enter quando estiver pronto...")
    flow = InstalledAppFlow.from_client_secrets_file(path, SCOPES)
    creds = flow.run_local_server(port=0, open_browser=True)
    data = {"client_id": creds.client_id, "client_secret": creds.client_secret, "refresh_token": creds.refresh_token}
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n✅ Autenticado! Refresh token:\n{creds.refresh_token}")
    print(f"\nPara GitHub Actions, define:\nGMAIL_CLIENT_ID={creds.client_id}\nGMAIL_CLIENT_SECRET={creds.client_secret}\nGMAIL_REFRESH_TOKEN={creds.refresh_token}")


def cmd_search(args):
    service = get_service()
    msgs = search_messages(service, args.query, args.max)
    if not msgs:
        print(f"Nenhuma mensagem para: {args.query}")
        return
    print(f"📧 {len(msgs)} encontrada(s):")
    for m in msgs:
        d = get_message_details(service, m["id"])
        print(f"\n  📌 [{d['date']}] {d['subject']}")
        print(f"     De: {d['from']}  |  ID: {d['id'][:20]}...")
        print(f"     {d['snippet'][:150]}")


def cmd_read(args):
    service = get_service()
    d = get_message_details(service, args.id)
    print(f"{'='*60}")
    print(f"Assunto: {d['subject']}")
    print(f"De:      {d['from']}")
    print(f"Para:    {d['to']}")
    print(f"Data:    {d['date']}")
    print(f"Thread:  {d['thread_id']}")
    print(f"{'='*60}")
    print(d["body"] or d["snippet"])


def cmd_reply(args):
    """Cria draft e mostra ao utilizador. NÃO envia automaticamente."""
    service = get_service()
    original = get_message_details(service, args.id)
    if not args.body:
        print("❌ Indica --body com o texto da resposta")
        sys.exit(1)
    draft = create_draft(service, original["from"], "Re: " + original["subject"], args.body, original["thread_id"])
    draft_id = draft["id"]
    print(f"{'='*60}")
    print(f"📝 RASCUNHO CRIADO (ID: {draft_id})")
    print(f"{'='*60}")
    print(f"Para:      {original['from']}")
    print(f"Assunto:   Re: {original['subject']}")
    print(f"{'='*60}")
    print(args.body)
    print(f"{'='*60}")
    print(f"\n✅ Rascunho guardado no Gmail. Envio NÃO executado.")
    print(f"   Para enviar: python3 scripts/gmail_monitor.py send-draft --id {draft_id}")
    print(f"   Para enviar directo: python3 scripts/gmail_monitor.py send --to \"{original['from']}\" --subject \"Re: {original['subject']}\" --body \"...\"")


def cmd_send(args):
    service = get_service()
    sent = send_message(service, args.to, args.subject, args.body, args.thread)
    print(f"✅ Enviado! ID: {sent['id']}")
    print(f"   Para: {args.to}  |  Assunto: {args.subject}")


def cmd_send_draft(args):
    service = get_service()
    sent = send_draft(service, args.id)
    print(f"✅ Draft enviado! ID: {sent['id']}")


def cmd_unread(args):
    service = get_service()
    inbox = service.users().labels().get(userId="me", id="INBOX").execute()
    total = inbox.get("messagesTotal", 0)
    unread = inbox.get("messagesUnread", 0)
    print(f"📬 Total: {total} | Não lidas: {unread}")
    if args.summary or unread == 0:
        return
    msgs = search_messages(service, "in:inbox is:unread", max_results=20)
    for m in msgs:
        d = get_message_details(service, m["id"])
        print(f"\n  [{d['date']}] {d['subject']}")
        print(f"  De: {d['from']}  |  ID: {d['id'][:20]}...")
        print(f"  {d['snippet'][:150]}")


def cmd_run(args):
    """Modo monitor completo — output JSON"""
    service = get_service()
    report = {"timestamp": datetime.utcnow().isoformat(), "unread": {}, "replies": [], "sent_today": []}
    try:
        inbox = service.users().labels().get(userId="me", id="INBOX").execute()
        total = inbox.get("messagesTotal", 0)
        unread = inbox.get("messagesUnread", 0)
        msgs = []
        if unread > 0:
            for m in search_messages(service, "in:inbox is:unread", max_results=10):
                d = get_message_details(service, m["id"])
                msgs.append({"from": d["from"], "subject": d["subject"], "date": d["date"], "snippet": d["snippet"][:200]})
        report["unread"] = {"total": total, "unread": unread, "messages": msgs}
    except Exception as e:
        report["unread"] = {"error": str(e)}
    print(json.dumps(report, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="MARC-Jarvis Gmail Assistant")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("auth", help="Autenticar OAuth 2.0")
    p.add_argument("--credentials", help="Caminho do credentials.json")

    p = sub.add_parser("search", help="Pesquisar emails")
    p.add_argument("--query", required=True)
    p.add_argument("--max", type=int, default=10)

    p = sub.add_parser("read", help="Ler email completo")
    p.add_argument("--id", required=True)

    p = sub.add_parser("reply", help="Criar rascunho de resposta (mostra, não envia)")
    p.add_argument("--id", required=True)
    p.add_argument("--body", required=True)

    p = sub.add_parser("send", help="Enviar email diretamente")
    p.add_argument("--to", required=True)
    p.add_argument("--subject", required=True)
    p.add_argument("--body", required=True)
    p.add_argument("--thread")

    p = sub.add_parser("send-draft", help="Enviar rascunho existente")
    p.add_argument("--id", required=True)

    p = sub.add_parser("unread", help="Listar não lidas")
    p.add_argument("--summary", action="store_true")

    sub.add_parser("run", help="Relatório completo (JSON)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    cmds = {
        "auth": cmd_auth,
        "search": cmd_search,
        "read": cmd_read,
        "reply": cmd_reply,
        "send": cmd_send,
        "send-draft": cmd_send_draft,
        "unread": cmd_unread,
        "run": cmd_run,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()

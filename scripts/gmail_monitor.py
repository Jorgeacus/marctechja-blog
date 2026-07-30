#!/usr/bin/env python3
"""
MARC-Jarvis — Gmail Monitor & Assistant
Ler, pesquisar, responder a emails via Gmail API.
Suporta múltiplas contas com nomes distintos.

Uso:
    python3 scripts/gmail_monitor.py auth --account pessoal
    python3 scripts/gmail_monitor.py auth --account radiestesia
    python3 scripts/gmail_monitor.py search --query "convite especial"
    python3 scripts/gmail_monitor.py search --account radiestesia --query "convite"
    python3 scripts/gmail_monitor.py read --id <msg_id>
    python3 scripts/gmail_monitor.py reply --id <msg_id> --body "..."
    python3 scripts/gmail_monitor.py send --to "x@y" --subject "..." --body "..."
    python3 scripts/gmail_monitor.py unread
    python3 scripts/gmail_monitor.py run --account radiestesia

Variáveis de ambiente (automação GitHub Actions):
    GMAIL_CLIENT_ID
    GMAIL_CLIENT_SECRET
    GMAIL_REFRESH_TOKEN_{ACCOUNT}  (ex: GMAIL_REFRESH_TOKEN_RADIESTESIA)
"""

import os, sys, json, base64, argparse, re
from datetime import datetime
from email.mime.text import MIMEText

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
]
TOKENS_FILE = os.path.expanduser("~/.marcjarvis_gmail_tokens.json")
CREDENTIALS_FILE = os.path.expanduser("~/.marcjarvis_gmail_credentials.json")
DEFAULT_ACCOUNT = "default"


def env_key(account):
    return f"GMAIL_REFRESH_TOKEN_{account.upper().replace('-','_')}"


def get_credentials(account):
    # Try env vars first (automation)
    client_id = os.environ.get("GMAIL_CLIENT_ID")
    client_secret = os.environ.get("GMAIL_CLIENT_SECRET")
    refresh_token = os.environ.get(env_key(account))
    if client_id and client_secret and refresh_token:
        return {"client_id": client_id, "client_secret": client_secret, "refresh_token": refresh_token}

    # Try default env vars
    refresh_token = os.environ.get("GMAIL_REFRESH_TOKEN")
    if client_id and client_secret and refresh_token:
        return {"client_id": client_id, "client_secret": client_secret, "refresh_token": refresh_token}

    # Fall back to tokens file
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE) as f:
            tokens = json.load(f)
        if account in tokens:
            return tokens[account]
        elif DEFAULT_ACCOUNT in tokens:
            return tokens[DEFAULT_ACCOUNT]

    return None


def get_service(account=DEFAULT_ACCOUNT):
    creds = get_credentials(account)
    if not creds:
        print(f"❌ Conta '{account}' não encontrada.")
        print(f"   Executa: python3 scripts/gmail_monitor.py auth --account {account}")
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
        for p in ([part] + part.get("parts", [])):
            if p.get("mimeType") == "text/plain" and "data" in p.get("body", {}):
                body = base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8", errors="replace")
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


def save_token(account, client_id, client_secret, refresh_token):
    tokens = {}
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE) as f:
            tokens = json.load(f)
    tokens[account] = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }
    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)
    print(f"  → Guardado como conta '{account}'")


# --- Commands ---

def cmd_auth(args):
    from google_auth_oauthlib.flow import InstalledAppFlow
    path = args.credentials or CREDENTIALS_FILE
    if not os.path.exists(path):
        print(f"❌ Credenciais não encontradas: {path}")
        print("1. https://console.cloud.google.com/apis/credentials")
        print("2. Criar 'OAuth 2.0 Client ID' → Desktop app")
        print("3. Download JSON →", path)
        sys.exit(1)
    account = args.account or DEFAULT_ACCOUNT
    print(f"🔑 A autenticar conta '{account}'...")
    input("Prima Enter quando tiveres o email de teste adicionado em https://console.cloud.google.com/apis/credentials/consent...")
    flow = InstalledAppFlow.from_client_secrets_file(path, SCOPES)
    creds = flow.run_local_server(port=0, open_browser=True)
    save_token(account, creds.client_id, creds.client_secret, creds.refresh_token)
    print(f"\n✅ Conta '{account}' autenticada!")
    print(f"Refresh token: {creds.refresh_token}")
    print(f"\nPara GitHub Actions, adiciona como secret:")
    print(f"  GMAIL_CLIENT_ID={creds.client_id}")
    print(f"  GMAIL_CLIENT_SECRET={creds.client_secret}")
    print(f"  {env_key(account)}={creds.refresh_token}")


def cmd_search(args):
    service = get_service(args.account)
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
    service = get_service(args.account)
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
    service = get_service(args.account)
    original = get_message_details(service, args.id)
    if not args.body:
        print("❌ Indica --body com o texto da resposta")
        sys.exit(1)
    subject = original["subject"]
    if not subject.startswith("Re:"):
        subject = "Re: " + subject
    message = MIMEText(args.body, _charset="utf-8")
    message["To"] = original["from"]
    message["Subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    draft_body = {"message": {"raw": raw, "threadId": original["thread_id"]}}
    draft = service.users().drafts().create(userId="me", body=draft_body).execute()
    draft_id = draft["id"]
    print(f"{'='*60}")
    print(f"📝 RASCUNHO CRIADO (ID: {draft_id})")
    print(f"{'='*60}")
    print(f"Conta:     {args.account}")
    print(f"Para:      {original['from']}")
    print(f"Assunto:   {subject}")
    print(f"{'='*60}")
    print(args.body)
    print(f"{'='*60}")
    print(f"\n✅ Rascunho guardado. Envio NÃO executado.")
    print(f"   Para enviar: python3 scripts/gmail_monitor.py send-draft --id {draft_id} --account {args.account}")


def cmd_send(args):
    service = get_service(args.account)
    message = MIMEText(args.body, _charset="utf-8")
    message["To"] = args.to
    message["Subject"] = args.subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    body = {"raw": raw}
    if args.thread:
        body["threadId"] = args.thread
    sent = service.users().messages().send(userId="me", body=body).execute()
    print(f"✅ Enviado! ID: {sent['id']}")
    print(f"   Conta: {args.account}  |  Para: {args.to}")


def cmd_send_draft(args):
    service = get_service(args.account)
    sent = service.users().drafts().send(userId="me", id=args.id).execute()
    print(f"✅ Draft enviado! ID: {sent['id']}")


def cmd_unread(args):
    service = get_service(args.account)
    inbox = service.users().labels().get(userId="me", id="INBOX").execute()
    total = inbox.get("messagesTotal", 0)
    unread = inbox.get("messagesUnread", 0)
    print(f"📬 [{args.account}] Total: {total} | Não lidas: {unread}")
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
    service = get_service(args.account)
    report = {"timestamp": datetime.utcnow().isoformat(), "account": args.account, "unread": {}}
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


def cmd_list(args):
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE) as f:
            tokens = json.load(f)
        if tokens:
            print("📋 Contas configuradas:")
            for acct in tokens:
                rt = tokens[acct]["refresh_token"][:20] + "..."
                print(f"  • {acct}  (refresh: {rt})")
            return
    print("Nenhuma conta configurada.")


def main():
    def make_parser():
        p = argparse.ArgumentParser(description="MARC-Jarvis Gmail Assistant")
        p.add_argument("--account", default=None, help=f"Nome da conta (defeito: {DEFAULT_ACCOUNT})")
        sub = p.add_subparsers(dest="command")

        def add_acct(sp):
            sp.add_argument("--account", help="Nome da conta (sobrepõe o global)")

        sp = sub.add_parser("auth", help="Autenticar OAuth 2.0")
        sp.add_argument("--credentials", help="Caminho do credentials.json")
        add_acct(sp)

        sub.add_parser("list", help="Listar contas configuradas")

        sp = sub.add_parser("search", help="Pesquisar emails")
        sp.add_argument("--query", required=True)
        sp.add_argument("--max", type=int, default=10)
        add_acct(sp)

        sp = sub.add_parser("read", help="Ler email completo")
        sp.add_argument("--id", required=True)
        add_acct(sp)

        sp = sub.add_parser("reply", help="Criar rascunho (mostra, não envia)")
        sp.add_argument("--id", required=True)
        sp.add_argument("--body", required=True)
        add_acct(sp)

        sp = sub.add_parser("send", help="Enviar email")
        sp.add_argument("--to", required=True)
        sp.add_argument("--subject", required=True)
        sp.add_argument("--body", required=True)
        sp.add_argument("--thread")
        add_acct(sp)

        sp = sub.add_parser("send-draft", help="Enviar rascunho")
        sp.add_argument("--id", required=True)
        add_acct(sp)

        sp = sub.add_parser("unread", help="Ver não lidas")
        sp.add_argument("--summary", action="store_true")
        add_acct(sp)

        sp = sub.add_parser("run", help="Relatório JSON")
        add_acct(sp)

        return p

    # Extract --account from argv before argparse to support both positions
    argv = sys.argv[1:]
    acct = None
    filtered = []
    i = 0
    while i < len(argv):
        if argv[i] == "--account" and i + 1 < len(argv):
            acct = argv[i + 1]
            i += 2
        elif argv[i].startswith("--account="):
            acct = argv[i].split("=", 1)[1]
            i += 1
        else:
            filtered.append(argv[i])
            i += 1

    parser = make_parser()
    args = parser.parse_args(filtered)
    args.account = acct or args.account or DEFAULT_ACCOUNT

    if not args.command:
        parser.print_help()
        return

    cmds = {
        "auth": cmd_auth, "list": cmd_list, "search": cmd_search,
        "read": cmd_read, "reply": cmd_reply, "send": cmd_send,
        "send-draft": cmd_send_draft, "unread": cmd_unread, "run": cmd_run,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()

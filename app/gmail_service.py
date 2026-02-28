import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

def authenticate_gmail():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def fetch_latest_email(service):
    results = service.users().messages().list(
        userId="me",
        maxResults=1
    ).execute()

    messages = results.get("messages", [])
    if not messages:
        return None

    msg = service.users().messages().get(
        userId="me",
        id=messages[0]["id"]
    ).execute()

    payload = msg["payload"]
    body = ""

    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"]["data"]
                body = base64.urlsafe_b64decode(data).decode()
    else:
        data = payload["body"]["data"]
        body = base64.urlsafe_b64decode(data).decode()

    return body

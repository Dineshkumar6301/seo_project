import os
import pickle
from pathlib import Path

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError as exc:
    raise ImportError(
        "Missing Google API dependencies. Install google-auth-oauthlib and google-api-python-client."
    ) from exc

SCOPES = [
    "https://www.googleapis.com/auth/webmasters.readonly"
]

BASE_DIR = Path(__file__).resolve().parents[1]
CLIENT_SECRET_FILE = BASE_DIR / "client_secret.json"
TOKEN_FILE = BASE_DIR / "token.pickle"


def get_gsc_service():
    creds = None

    if TOKEN_FILE.exists():
        with TOKEN_FILE.open("rb") as token:
            creds = pickle.load(token)

    if not creds:
        if not CLIENT_SECRET_FILE.exists():
            raise FileNotFoundError(
                f"Google client secrets file not found: {CLIENT_SECRET_FILE}. "
                "Create or move client_secret.json to the project root."
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            SCOPES
        )

        creds = flow.run_local_server(
            host="localhost",
            port=8080,
            open_browser=True
        )

        with TOKEN_FILE.open("wb") as token:
            pickle.dump(creds, token)

    service = build(
        "searchconsole",
        "v1",
        credentials=creds
    )

    return service
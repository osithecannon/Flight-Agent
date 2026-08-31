import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_calendar_service():
  creds = None
  # Look for token.json in the root directory (one level up from app/)
  token_path = os.path.abspath(
      os.path.join(os.path.dirname(__file__), "..", "token.json")
  )
  creds_path = os.path.abspath(
      os.path.join(os.path.dirname(__file__), "..", "credentials.json")
  )

  if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
      # Use manual flow fallback if running on headless server
      flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
      auth_url, _ = flow.authorization_url(prompt="consent")
      raise Exception(
          f"Token missing or expired on server. Please authorize locally or set"
          f" up token correctly. Auth URL: {auth_url}"
      )

  return build("calendar", "v3", credentials=creds)

import datetime
import os.path
from pathlib import Path
from venv import create

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

BASE_DIR = Path(__file__).resolve().parents[2]
CREDENTIALS_PATH = BASE_DIR / "credentials.json"
TOKEN_PATH = BASE_DIR / "token.json"
def create_credential(): 
  creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
  if os.path.exists(str(TOKEN_PATH)):
      creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(CREDENTIALS_PATH), SCOPES
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open(str(TOKEN_PATH), "w") as token:
        token.write(creds.to_json())
    
  return creds

def get_google_service(api_name: str):
  cres = create_credential()
  return build(api_name, "v3", credentials=cres)

get_google_service("calendar")
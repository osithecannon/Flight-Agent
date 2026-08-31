import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            
            # Detect Google Colab environment
            try:
                from google.colab import output
                # Use a fixed redirect URI for Colab / headless execution
                flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
                auth_url, _ = flow.authorization_url(prompt='consent')
                print(f"\n1. Open this URL in your browser:\n{auth_url}\n")
                code = input("2. Enter the authorization code here: ").strip()
                flow.fetch_token(code=code)
                creds = flow.credentials
            except Exception:
                # Fallback for standard local execution
                creds = flow.run_local_server(port=0)
                
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return build('calendar', 'v3', credentials=creds)

def get_free_dates(start_date_str: str, end_date_str: str) -> list:
    """Returns a list of dates (YYYY-MM-DD) that have no primary calendar events."""
    service = get_calendar_service()
    time_min = f"{start_date_str}T00:00:00Z"
    time_max = f"{end_date_str}T23:59:59Z"
    
    events_result = service.events().list(
        calendarId='primary', timeMin=time_min, timeMax=time_max,
        singleEvents=True, orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    busy_dates = set()
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        busy_dates.add(start[:10])
    
    start_dt = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_dt = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
    all_dates = [(start_dt + datetime.timedelta(days=i)).strftime("%Y-%m-%d") 
                 for i in range((end_dt - start_dt).days + 1)]
    
    return [date for date in all_dates if date not in busy_dates]
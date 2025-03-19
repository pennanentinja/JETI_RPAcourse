import os
import pickle
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# File path that contains the user's Google account login credentials.
CREDENTIALS_FILE = 'credentials.json'

# Permissions required to use the Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Function to log in to the Google Calendar API.
def authenticate_google_account():
    creds = None
    # If the user has previously saved login credentials, load them.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no valid login credentials, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the login credentials to a file so that they don't need to be asked for again.
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

# Function that fetches Google Calendar events.
def get_calendar_events():
    creds = authenticate_google_account()
    
    # Build a service with the Google Calendar API.
    service = build('calendar', 'v3', credentials=creds)
    
    # Fetch events in the near future (e.g., the next 7 days).
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    
    if not events:
        print('\nNo tasks or events found.')
    else:
        print('\nFuture tasks and events:')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"{event['summary']} ({start})")

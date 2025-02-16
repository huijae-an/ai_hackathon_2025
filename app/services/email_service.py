import os.path
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Authenticate and return the Gmail API service."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def list_messages(service, user_id='me', max_results=10, days = 3):
    date_from = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')
    query = f"after:{date_from}"
    results = service.users().messages().list(userId=user_id, q = query, maxResults=max_results).execute()
    return results.get('messages', [])

def get_message(service, msg_id, user_id='me'):
    """Retrieve a single message by ID."""
    message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
    return message

def extract_email_data(message):
    """Extract subject and body from a Gmail message."""
    headers = message.get('payload', {}).get('headers', [])
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
    body = ""
    
    parts = message.get('payload', {}).get('parts', [])
    if parts:
        body_data = parts[0].get('body', {}).get('data', '')
        if body_data:
            body = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
    return subject, body

def get_emails():
    """
    Fetches emails from Gmail using the Gmail API.
    
    Returns:
        A list of dictionaries with each dictionary having:
        {"subject": ..., "body": ...}
    """
    service = get_gmail_service()
    messages = list_messages(service, max_results = 10)
    emails = []
    for msg in messages:
        message = get_message(service, msg['id'])
        subject, body = extract_email_data(message)
        emails.append({"subject": subject, "body": body})
    return emails


import os
import json
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from ai_agent.state import GraphState


# Google Calendar full access
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def authenticate_google():
    """Authenticate and return Google Calendar service."""
    creds = None
    if os.path.exists("ai_agent/token.json"):
        creds = Credentials.from_authorized_user_file("ai_agent/token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("ai_agent/credentials.json", SCOPES)
            creds = flow.run_local_server(port=8080)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)

def settask_in_calendar(state: GraphState) -> str:
    """
    Create a new event in the user's Google Calendar.

    Args:
        start_time (str): Start datetime in ISO format (e.g., '2025-07-02T14:00:00+05:30')
        end_time (str): End datetime in ISO format
        task (str): Title/description of the task

    Returns:
        str: Event link if created successfully
    """
    try:
        print("---SETTING TASK IN GOOGLE CALENDAR---")
        service = authenticate_google()
        event = {
            'summary': state['task'],
            'description': 'Scheduled by TailorTalk AI',
            'start': {
                'dateTime': state['start_time'].isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': state['end_time'].isoformat(),
                'timeZone': 'UTC',
            }
        }


        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print("---TASK SCHEDULED SUCCESSFULLY---")

        return {
            "event_link":created_event.get("htmlLink")
        }

    except Exception as e:
        print(" Error scheduling task:", e)
        return ""


import datetime
import os
import json
from typing import List, Dict, Any
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from ai_agent.state import GraphState
from datetime import timezone


SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Ensure datetime is timezone-aware and in UTC
def ensure_utc(dt: datetime.datetime) -> datetime.datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc)

# Google Calendar authentication
def authenticate_google():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=8080)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)

# Get busy slots from Google Calendar
def get_busy_slots(service, start: datetime.datetime, end: datetime.datetime) -> List[Dict[str, str]]:
    body = {
        "timeMin": start.isoformat(),
        "timeMax": end.isoformat(),
        "timeZone": "UTC",
        "items": [{"id": "primary"}],
    }
    result = service.freebusy().query(body=body).execute()
    return result["calendars"]["primary"].get("busy", [])

# Check if slot overlaps with any busy slot
def is_slot_available(start_dt: datetime.datetime, end_dt: datetime.datetime, busy_slots: List[Dict[str, str]]) -> bool:
    start_dt = ensure_utc(start_dt)
    end_dt = ensure_utc(end_dt)

    for slot in busy_slots:
        busy_start = ensure_utc(datetime.datetime.fromisoformat(slot['start']))
        busy_end = ensure_utc(datetime.datetime.fromisoformat(slot['end']))
        if start_dt < busy_end and end_dt > busy_start:
            return False
    return True

# Find 1-hour free slots in the window
def find_free_slots(busy_slots, window_start, window_end, slot_minutes=60) -> List[Dict[str, str]]:
    suggestions = []
    delta = datetime.timedelta(minutes=slot_minutes)
    current = window_start

    while current + delta <= window_end:
        slot_start = current
        slot_end = current + delta
        if is_slot_available(slot_start, slot_end, busy_slots):
            suggestions.append({
                "start": slot_start.isoformat(),
                "end": slot_end.isoformat()
            })
        current += delta

    return suggestions

# Main logic to check and suggest
def check_and_suggest_around_task(state: GraphState) -> Dict[str, Any]:
    print("---CHECKING AVAILABILITY---")
    service = authenticate_google()

    # Ensure UTC timezone
    start_dt = ensure_utc(state["start_time"])
    end_dt = ensure_utc(state["end_time"])
    window_start = ensure_utc(start_dt - datetime.timedelta(days=7))
    window_end = ensure_utc(end_dt + datetime.timedelta(days=7))

    # Fetch busy slots
    busy_slots = get_busy_slots(service, window_start, window_end)
    print(f"Busy slots: {busy_slots}")

    # Check availability
    if is_slot_available(start_dt, end_dt, busy_slots):
        print(" Slot is available")
        return {"available": True, "suggestions": []}

    # Suggest alternatives
    suggestions = find_free_slots(busy_slots, window_start, window_end)
    print(" Slot is busy. Suggested alternatives:")

    return {
        "available": False,
        "suggestions": suggestions
    }


# # === Example usage ===
# if __name__ == "__main__":
#     start = "2025-06-04T15:00:00+05:30"
#     end = "2025-07-04T16:00:00+05:30"
    
#     result = check_and_suggest_around_task(start, end)


#     if result["available"]:
#         print(f" Slot is available: {start} to {end}")
#     else:
#         print(f" Slot is NOT available: {start} to {end}")
#         print(" Suggested Free Slots:")
#         for slot in result["suggestions"]:
#             print(f"  - {slot['start']} to {slot['end']}")

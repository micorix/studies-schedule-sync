from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from lib.settings import settings

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

CREDS_DIR = "./.creds"
TOKEN_FILE_PATH = os.path.join(CREDS_DIR, "token.json")
CREDENTIALS_FILE_PATH = os.path.join(CREDS_DIR, "credentials.json")


def get_gcal_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("Reusing token credentials")
        else:
            print("Initiating login flow")
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE_PATH, "w") as token:
            token.write(creds.to_json())

    if not creds:
        raise Exception("No creds provided")

    return build("calendar", "v3", credentials=creds)


def is_calendar_empty(service, calendar_id):
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=1,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    return len(events) == 0


def list_calendars(service):
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list["items"]:
            yield calendar_list_entry
        page_token = calendar_list.get("nextPageToken")
        if not page_token:
            break


def recreate_calendar(service):
    # Workaround. Clearing non-primary calendar throws 400 error
    for cal in list_calendars(service):
        if cal["summary"] == settings.calendar_name:
            service.calendars().delete(calendarId=cal["id"]).execute()
            break

    calendar = {"summary": settings.calendar_name, "timeZone": settings.timezone_city}

    created_calendar = service.calendars().insert(body=calendar).execute()
    return created_calendar["id"]


def regenerate_calendar(events):
    service = get_gcal_service()

    calendar_id = recreate_calendar(service)

    for event in events:
        service.events().insert(calendarId=calendar_id, body=event).execute()
        print(
            f"Inserting event {event.get('summary')} (starts at {event.get('start').get('dateTime')})"  # noqa: 501
        )

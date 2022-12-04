from __future__ import print_function

import datetime
import os.path

from google.oauth2 import service_account
from googleapiclient.discovery import build

from lib.settings import settings

SCOPES = ["https://www.googleapis.com/auth/calendar"]

CREDS_DIR = "./.creds"
SERVICE_ACCOUNT_FILE_PATH = os.path.join(CREDS_DIR, "service-account.json")


def get_gcal_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE_PATH, scopes=SCOPES
    )
    return build("calendar", "v3", credentials=credentials)


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
            print("Deleting previous calendar")
            break

    calendar = {"summary": settings.calendar_name, "timeZone": settings.timezone_city}

    created_calendar = service.calendars().insert(body=calendar).execute()
    print(f"Recreated {settings.calendar_name} calendar")
    return created_calendar["id"]


def regenerate_calendar(events):
    service = get_gcal_service()

    calendar_id = recreate_calendar(service)

    for event in events:
        service.events().insert(calendarId=calendar_id, body=event).execute()
        print(
            f"Inserting event {event.get('summary')} (starts at {event.get('start').get('dateTime')})"  # noqa: 501
        )

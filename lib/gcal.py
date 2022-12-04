from __future__ import print_function

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


def get_calendar_events(service, calendar_id):
    page_token = None
    while True:
        events = (
            service.events()
            .list(calendarId=calendar_id, pageToken=page_token)
            .execute()
        )
        for event in events["items"]:
            yield event
        page_token = events.get("nextPageToken")
        if not page_token:
            break


def clear_calendar(service, calendar_id):
    # Workaround. calling calendar.clear() on non-primary calendar throws 400 error
    events_to_delete = get_calendar_events(service, calendar_id)
    for event in events_to_delete:
        service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()

    print("Cleared calendar")


def regenerate_calendar(events):
    service = get_gcal_service()

    clear_calendar(service, settings.calendar_id)

    for event in events:
        service.events().insert(calendarId=settings.calendar_id, body=event).execute()
        print(
            f"Inserting event {event.get('summary')} (starts at {event.get('start').get('dateTime')})"  # noqa: 501
        )

import re

from lib.datatypes import ScheduleEventInfo
from lib.settings import settings


def stringify_datetime(date_str, h_str):
    return f"{date_str}T{h_str}:00"


def map_schedule_event_to_gcal_event(schedule_event: ScheduleEventInfo):
    print(schedule_event)
    name = schedule_event.get("name")
    match = re.match(r"^(.*) - \((.*)\)", name)  # <subject name> - (<event type>)

    name = match.group(1)
    event_type = match.group(2)

    return {
        "summary": name,
        "location": f"{settings.university_location} at {schedule_event.get('location')}",
        "description": f"Type: {event_type}",
        "start": {
            "dateTime": stringify_datetime(
                schedule_event.get("date"), schedule_event.get("time").get("start")
            ),
            "timeZone": settings.timezone_city,
        },
        "end": {
            "dateTime": stringify_datetime(
                schedule_event.get("date"), schedule_event.get("time").get("end")
            ),
            "timeZone": settings.timezone_city,
        },
    }

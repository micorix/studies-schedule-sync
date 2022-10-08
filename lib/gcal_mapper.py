from lib.datatypes import ScheduleEventInfo
from lib.settings import settings


def stringify_datetime(date_str, h_str):
    return f"{date_str}T{h_str}:00{settings.timezone_gmt}"


def map_schedule_event_to_gcal_event(schedule_event: ScheduleEventInfo):
    print(schedule_event)
    return {
        "summary": schedule_event.get("name"),
        "location": settings.university_location,
        "description": "\n".join(
            [
                f"Location: {schedule_event.get('location')}",
                f"Type: {schedule_event.get('event_type')}",
            ]
        ),
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
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 60},
                {"method": "popup", "minutes": 10},
            ],
        },
    }

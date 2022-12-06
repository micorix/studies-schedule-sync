from lib.datatypes import ScheduleEventInfo
from lib.settings import settings


def stringify_datetime(date_str, h_str):
    return f"{date_str}T{h_str}:00"


def map_schedule_event_to_gcal_event(schedule_event: ScheduleEventInfo):
    print(schedule_event)
    type = schedule_event.get('event_type')
    if schedule_event.get('event_type') == "(w)":
        type = "Wykład"
    elif schedule_event.get('event_type') == "(ć)":
        type = "Ćwiczenia"
    elif schedule_event.get('event_type') == "(L)":
        type = "Labolatoria"
    name = schedule_event.get("name")

    return {
        "summary": name.strip(
            " - (Wykład)").strip(" - (Ćwiczenia)").strip(" - (Labolatoria)"),
        "location": settings.university_location + ' at ' + schedule_event.get('location'),
        "description": "\n".join(
            [
                f"Type: {type}",
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
    }

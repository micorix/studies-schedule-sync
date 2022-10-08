import requests

from lib.gcal import regenerate_calendar
from lib.gcal_mapper import map_schedule_event_to_gcal_event
from lib.schedule_parser import parse_events_from_schedule
from lib.settings import settings


def main():
    r = requests.get(settings.schedule_page_url)
    events = parse_events_from_schedule(r.content)
    print(list(events))
    events = map(map_schedule_event_to_gcal_event, events)
    print(list(events))
    regenerate_calendar(events)


if __name__ == "__main__":
    main()

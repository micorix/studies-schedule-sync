import requests

from lib.gcal import regenerate_calendar
from lib.gcal_mapper import map_schedule_event_to_gcal_event
from lib.schedule_parser import parse_events_from_schedule
from lib.settings import settings


def main():
    # XXX(micorix): verify=false due to strange config of the old site:
    # there is cert problem with the old faculty site, so tried it without https
    # but when accessing it via http, it redirects to the new site which doesn't have schedule page yet
    # bc the old page will be deprecated soon, this quick fix was introduced
    r = requests.get(settings.schedule_page_url, verify=False)
    events = parse_events_from_schedule(r.content)
    events = map(map_schedule_event_to_gcal_event, events)
    regenerate_calendar(events)


if __name__ == "__main__":
    main()

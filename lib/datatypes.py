from typing import TypedDict


class EventTimeBoundaries(TypedDict):
    start: str
    end: str


class ScheduleEventInfo(TypedDict):
    name: str
    short_name: str
    event_type: str
    location: str

    block_no: int
    time: EventTimeBoundaries
    date: str

from __future__ import annotations

from typing import Dict

from bs4 import BeautifulSoup

from lib.datatypes import ScheduleEventInfo, EventTimeBoundaries


def extract_date_from_day_container_class_name(class_name: [str]) -> str:
    element_class_name = class_name
    element_class_name.remove("day")
    element_class_name = element_class_name[0]
    return element_class_name.replace("_", "-")


def get_additional_event_info_from_name_contents(name_contents) -> Dict[str, str]:
    content_list = [str(x) for x in name_contents]
    return {
        "short_name": content_list[0],
        "event_type": content_list[2],
        "location": content_list[4],
    }


def get_time_boundaries_by_block_id(block_nr_element):
    start = block_nr_element.find("span", class_="hr1").text
    end = block_nr_element.find("span", class_="hr2").text
    return EventTimeBoundaries(start=start, end=end)


def parse_events_from_schedule(site_content):
    soup = BeautifulSoup(site_content, "html5lib")
    schedule_container = soup.find("div", class_="lessons")

    for lesson_container in schedule_container.find_all("div", class_="lesson"):
        name = lesson_container.find("span", class_="info").text
        date = lesson_container.find("span", class_="date").text.replace("_", "-")
        block_id = lesson_container.find("span", class_="block_id").text
        block_no = int(block_id.replace("block", ""))
        additional_info = get_additional_event_info_from_name_contents(
            lesson_container.find("span", class_="name").contents
        )

        time_boundaries = get_time_boundaries_by_block_id(
            soup.find("div", class_=block_id)
        )

        yield ScheduleEventInfo(
            name=name,
            short_name=additional_info["short_name"],
            event_type=additional_info["event_type"],
            location=additional_info["location"],
            time=time_boundaries,
            date=date,
            block_no=block_no,
        )

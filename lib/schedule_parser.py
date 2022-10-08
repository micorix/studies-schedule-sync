from __future__ import annotations

from bs4 import BeautifulSoup

from lib.datatypes import ScheduleEventInfo, EventTimeBoundaries


def extract_date_from_day_container_class_name(class_name: [str]) -> str:
    element_class_name = class_name
    element_class_name.remove("day")
    element_class_name = element_class_name[0]
    return element_class_name.replace("_", "-")


def get_event_info_from_block(block) -> ScheduleEventInfo | None:
    if "title" not in block.attrs:
        return None

    content_list = [str(x) for x in block.contents]

    return ScheduleEventInfo(
        name=block.attrs["title"].strip(),
        short_name=content_list[0],
        event_type=content_list[2],
        location=content_list[4],
    )


def get_blocks_time_boundaries(day_blocks_container):
    time_boundaries = {}
    for block in day_blocks_container.find_all("div", class_="block_nr"):
        block_no = block.find("span", class_="nr").text
        start = block.find("span", class_="hr1").text
        end = block.find("span", class_="hr2").text
        time_boundaries[int(block_no)] = EventTimeBoundaries(start=start, end=end)
    return time_boundaries


def parse_events_from_schedule(site_content):
    soup = BeautifulSoup(site_content)
    schedule_container = soup.find("div", class_="rozklad_container")

    for week_day_container in schedule_container.find_all("div", class_="day_v1"):
        blocks_time_boundaries = get_blocks_time_boundaries(
            week_day_container.find("div", class_="day_blocks")
        )

        days_container = week_day_container.find("div", class_="days")
        single_day_containers = days_container.find_all("div", class_="day")

        for single_day_container in single_day_containers:
            date = extract_date_from_day_container_class_name(
                single_day_container["class"]
            )

            for i, block in enumerate(
                single_day_container.find_all("div", class_="block")
            ):
                event_info = get_event_info_from_block(block)
                if event_info:
                    block_no = i + 1
                    event_info["block_no"] = block_no
                    event_info["time"] = blocks_time_boundaries[block_no]
                    event_info["date"] = date

                    yield event_info

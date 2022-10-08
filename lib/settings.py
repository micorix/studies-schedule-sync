import os
from dotenv import load_dotenv

load_dotenv()


def get_from_env_var(env_var_name, fallback=""):
    from_env = os.environ.get(env_var_name, fallback).strip()
    if not from_env:
        raise Exception(f"Setup {env_var_name} env var")
    return from_env


class Settings:
    @property
    def schedule_page_url(self):
        return get_from_env_var("SCHEDULE_PAGE_URL")

    @property
    def university_location(self):
        return get_from_env_var("UNIVERSITY_LOCATION")

    @property
    def timezone_gmt(self):
        return get_from_env_var("TIMEZONE_GMT", "+02:00")

    @property
    def timezone_city(self):
        return get_from_env_var("TIMEZONE_CITY", "Europe/Warsaw")

    @property
    def calendar_name(self):
        return get_from_env_var("STUDIES_CALENDAR_NAME", "__STUDIES_SCHEDULE__")


settings = Settings()

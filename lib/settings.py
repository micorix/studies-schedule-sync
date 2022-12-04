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
    def calendar_id(self):
        return get_from_env_var("CALENDAR_ID")

    @property
    def schedule_page_url(self):
        return get_from_env_var("SCHEDULE_PAGE_URL")

    @property
    def university_location(self):
        return get_from_env_var("UNIVERSITY_LOCATION")

    @property
    def timezone_city(self):
        return get_from_env_var("TIMEZONE_CITY", "Europe/Warsaw")


settings = Settings()

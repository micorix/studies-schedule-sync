# Studies schedule sync

Little script which syncs schedule from some page and places it in Google Calendar. 

Ultimately used in CI with cron as a trigger.

[See here for the example](.github/workflows/sync_with_gcal.yml)

**:warning: Note: Please still check original schedule page. I did my best but I can't guarantee that this script works 100% of the time. If you stumble across some bug, please open an issue or submit a PR**

## Usage

Prerequisites:
* [Enable Google Calendar API](https://developers.google.com/calendar/api/quickstart/python#enable_the_api)
* [Create GCP service account](https://medium.com/@ArchTaqi/google-calendar-api-in-your-application-without-oauth-consent-screen-4fcc1f8eb380)
  * Download service account JSON key and place it as `service-account.json` file in `.creds` dir.
* Create a calendar in Google Calendar
* Share that calendar with GCP service account with (`edit` permission)
* Setup env vars

Requirements:
* Python >= 3.8
* watchman
* poetry


```shell
poetry install
poetry run python main.py
```

### Env vars

| Name | Required | Description |
| - | :-: | - |
| `SCHEDULE_PAGE_URL` | :heavy_check_mark: | URL of schedule page. Look out for the query (such as `?groupId=XXX`) |
| `CALENDAR_ID` | :heavy_check_mark: | Calendar id. Something like `XXX@group.calendar.google.com` |
| `UNIVERSITY_LOCATION` | :heavy_check_mark: | University location. |
| `TIMEZONE_CITY` | :x: | e.g. "America/Los_Angeles", "Europe/Warsaw". "Europe/Warsaw" by default |

You can place env vars in `.env` file.

### Running script in GitHub Actions

The primary purpose of this script is for it to be run in CI with cron trigger.

You can find an example of running this in gh actions in `.github/workflows` dir. 
To use it for yourself, fork this repo and substitute relevant constants & secrets.

[See here for the example](.github/workflows/sync_with_gcal.yml) 

**Remember to place `service-account.json` file contents as a secret.**
### Caveats

Clearing non-primary calendar throws error 400. I couldn't get to the cause so for now all events in calendar will be deleted one by one every time script runs.

The problem with this solution is that: 
1. it takes longer
2. any manual changes to the calendar won't be saved

A possible solution is to update events in place but idk if any optimization at this stage is needed. 

### Linter & formatter

`poetry run flake8`
`poetry run black .`

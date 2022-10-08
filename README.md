# Studies schedule sync

Little script which syncs schedule from some page and places it in Google Calendar. 

Ultimately used in CI with cron as a trigger.

[See here for the example](.github/workflows/sync_with_gcal.yml) 

## Usage

Prerequisites:
* [Enable Google Calendar API](https://developers.google.com/calendar/api/quickstart/python#enable_the_api)
* [Authorize credentials for a desktop application](https://developers.google.com/calendar/api/quickstart/python#authorize_credentials_for_a_desktop_application)
  * Place `credentials.json` file in `.creds` dir.
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
| `UNIVERSITY_LOCATION` | :heavy_check_mark: | University location. |
| `TIMEZONE_GMT` | :x: | e.g. "+2:00", "-7:00". "+2:00" by default |
| `TIMEZONE_CITY` | :x: | e.g. "America/Los_Angeles", "Europe/Warsaw". "Europe/Warsaw" by default |
| `STUDIES_CALENDAR_NAME` | :x: | `__STUDIES_SCHEDULE__` by default. Beware, calendar with this name will be recreated every time script run. |

You can place env vars in `.env` file.

### Running script in GitHub Actions

The primary purpose of this script is for it to be run in CI with cron trigger.

You can find an example of running this in gh actions in `.github/workflows` dir. 
To use it for yourself, clone this repo and substitute relevant constants & secrets.

[See here for the example](.github/workflows/sync_with_gcal.yml) 

**Remember to place `token.json` file contents as a secret.**
You can get it by running the script locally and aborting after logging in using popup.

### Caveats

Clearing non-primary calendar throws error 400. I couldn't get to the cause so for now calendar with given name will be deleted and recreated every time script runs.

The problem with this solution is that: 
1. it takes longer
2. `calendarId` will be different every time
3. any manual changes to the calendar won't be saved

If you come up with some clever solution how to solve it, feel free to submit a PR
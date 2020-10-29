# sheetcal
An ugly script to create events with reminders in Google Calendar for upcoming public mocks (for https://t.me/FaangInterview).

What you need to make it work:
* Python3
* Install necessary modules:

  ```pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```
* Create a project in [Google Developer Console](https://console.developers.google.com/apis/dashboard), enable Google Calendar API and Google Sheets API for it. Create credentials for this project (OAuth 2.0 Client IDs, type: Desktop) and download credentials.json file into the project's root

Run it with the mock schedule spreadsheet id as follows:

 ```SHEETS_ID=... python3 sheetcal.py```

When run for the first time, the script will ask to authorize the project to use Google Calendar and Google Sheets. It will read the spreadsheet and create events in your primary calendar. It won't create duplicates, so it can be launched many times.

Current limitation is that the script is not updating events with new information, only creating new ones.

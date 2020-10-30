# sheetcal
An ugly script to create events with reminders in Google Calendar for upcoming public mocks (for https://t.me/FaangInterview).

What you need to make it work:
* Python3
* Install necessary modules:

  ```pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib```
* Create a project in [Google Developer Console](https://console.developers.google.com/apis/dashboard), enable Google Calendar API and Google Sheets API for it. Create credentials for this project (OAuth 2.0 Client IDs, type: Desktop) and download credentials.json file into the project's root

Run it with the mock schedule spreadsheet id as follows:

 ```SHEETS_ID=... python3 sheetcal.py```

When run for the first time, the script will ask to authorize the project to use Google Calendar and Google Sheets. It will read the spreadsheet and create events in your primary calendar. It won't create duplicates, so it can be launched many times. If some information has changed - the event will be updated.

Another thing to keep in mind is that the spreadsheet is evolving and edited by people, so you might encounter errors and could need to reconfigure some things - like cell ranges, time formats, etc. There are some constants for that at the top of the script for convenience.

Disclaimer: *there is no license or any kind of warranty here, use it at your own risk.*

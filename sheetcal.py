#!/usr/bin/env python3

from __future__ import print_function
import pickle
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/calendar.events']

# The ID and range of a sample spreadsheet.
SHEET_ID = '18odJizS8jKHVpXHzItAyTTR7djOrcyk2Gi3Za4krtmg'
RANGE_NAME = 'A4:E10'

def main():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    sheets_svc = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = sheets_svc.spreadsheets()
    mocks = sheet.values().get(spreadsheetId=SHEET_ID,
                                range=RANGE_NAME).execute()
    values = mocks.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            try:
                dt = datetime.datetime.strptime(row[0], '%a %d.%m %H:%M').replace(year = datetime.datetime.now().year)
                print(f'{dt}')
            except ValueError:
                pass


    calendar_svc = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = calendar_svc.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import os.path
from datetime import datetime, timedelta
from pytz import timezone
import sys
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
          'https://www.googleapis.com/auth/calendar.events']

# The ID and range of the public mocks_in_sheet spreadsheet.
SHEET_ID = '18odJizS8jKHVpXHzItAyTTR7djOrcyk2Gi3Za4krtmg'
RANGE_NAME = 'A4:E8'

MOCK_TOPIC_TAG = 'Mock Interview'
MOCK_DURATION = timedelta(hours=1)
MOCK_TIMEZONE = 'Europe/Berlin'


def add_mock_event(calendar_svc, row):
    if not row or len(row) == 0:
        return
    mock_title = f'{MOCK_TOPIC_TAG}: {row[1]} vs {row[2]}'
    try:
        start_time = datetime.strptime(row[0], '%a %d.%m %H:%M').replace(
            year=datetime.now().year)
        start_time = timezone(MOCK_TIMEZONE).localize(start_time)
        if start_time < datetime.now(tz=timezone(MOCK_TIMEZONE)):
            print(f"You've missed this one already: {start_time}, skipping it")
            return
        existing_mock_events = calendar_svc.events().list(calendarId='primary',
                                                          timeMin=start_time.isoformat(), timeMax=(start_time + MOCK_DURATION).isoformat(), q=f'{MOCK_TOPIC_TAG}', singleEvents=True).execute().get('items', [])
        if existing_mock_events:
            print(f'Skipping existing event {row}')
            return
        mock_description = f'{mock_title}'
        if len(row) >= 4:
            mock_description += f'\n\n{row[3]}'
            if len(row) >= 5:
                mock_description += f'\n\n{row[4].removeprefix("Description:")}'
        new_mock_event = {
            'summary': f'{mock_title}',
            'description': mock_description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': MOCK_TIMEZONE,
            },
            'end': {
                'dateTime': (start_time + MOCK_DURATION).isoformat(),
                'timeZone': MOCK_TIMEZONE,
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        calendar_svc.events().insert(calendarId='primary', body=new_mock_event).execute()
    except Exception as e:
        print(e, file=sys.stderr)


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
    mocks_in_sheet = sheet.values().get(spreadsheetId=SHEET_ID,
                                        range=RANGE_NAME).execute()
    values = mocks_in_sheet.get('values', [])

    calendar_svc = build('calendar', 'v3', credentials=creds)

    if not values:
        print('No data found.')
    else:
        for row in values:
            # add a mock event to calendar
            add_mock_event(calendar_svc, row)

    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    future_mocks_in_calendar = calendar_svc.events().list(calendarId='primary',
                                                          timeMin=now, q=f'{MOCK_TOPIC_TAG}', singleEvents=True).execute().get('items', [])
    print("Future mocks in calendar:")
    for event in future_mocks_in_calendar:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()

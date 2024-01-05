import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_credentials():
    print("11")

    creds = None

    if os.path.exists('CREDENTIALS/token.json'):
        print("toekn exists")
        creds = Credentials.from_authorized_user_file('CREDENTIALS/token.json')
        print("exists 2")

    print("exists 3")

    print(creds.valid)

    if not creds or not creds.valid:
        print("toen exists 4 ")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow  = InstalledAppFlow.from_client_secrets_file('CREDENTIALS/token.json',SCOPES)

            creds = flow.run_local_server(port=0)

            with open('CREDENTIALS/token.json','w') as token:
                token.write(creds.to_json())

        print("get cred")
    print("exists 5")

    return creds

def create_event(service,appointment):
    try:

        start_datetime = f"{appointment.date}T{appointment.start_time}:00"  
        end_datetime = appointment.end_time.strftime('%Y-%m-%dT%H:%M:%S') 

        event = {
            'summary': f'Appointment with {appointment.patient.username}',
            # 'location': '800 Howard St., San Francisco, CA 94103',
            'description': f'New appointment with patient {appointment.patient.username} regarding {appointment.specialty}',
            'start': {
                'dateTime': f'{start_datetime}',
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': f'{end_datetime}',
                'timeZone': 'Asia/Kolkata',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=2'
            ],
            # 'attendees': [
            #     {'email': 'lpage@example.com'},
            #     {'email': 'sbrin@example.com'},
            # ]
        } 

        created_event =  service.events().insert(calendarId='primary', body=event).execute()
        print (f'Event created: {created_event.get("htmlLink")}')
    except HttpError as e:
        print("An error occured: ",e)

def main(appointment):
    creds = get_credentials()

    service = build("calendar", "v3", credentials=creds)

    create_event(service,appointment)

if __name__ == 'main':
    print("000")
    main ()


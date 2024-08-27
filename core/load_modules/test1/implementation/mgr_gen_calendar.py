from typing import Type
from data_module import QueryContext, DataInterface, DataManagerInterface, DataNodeContext, FunctionNodeContext
from . import Calendar, CalendarList
import os.path
import os
from dateutil import parser
import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

class CalendarManager(DataManagerInterface):
    @staticmethod
    def set_service_response(response, ctx: FunctionNodeContext):
        if isinstance(response, (Calendar, CalendarList)):
            ctx.set_query_response(response)
        else:
            raise ValueError("Response must be an instance of DataInterface")

    @staticmethod
    def get_descriptor_class(desc_index:int)->Type:
        if desc_index == 0:
            return Calendar
        elif desc_index == 1:
            return CalendarList
        else:
            raise ValueError("Invalid Descriptor Index")
    @staticmethod
    def get_descriptor(desc_index:int, ctx:DataNodeContext) -> DataInterface :
        if desc_index == 0:
            return CalendarManager._single(ctx)
        elif desc_index == 1:
            return CalendarManager._list(ctx)
        elif desc_index == 2:
            return CalendarManager._previous(ctx)
        else:
            raise ValueError("Invalid Descriptor Index")

    @staticmethod
    def _single( ctx: DataNodeContext) -> DataInterface :
        calendar_list_obj = CalendarList(calendar_list=[])
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

        service = build("calendar", "v3", credentials=creds)

        page_token = None
        while True:
            events = service.events().list(calendarId='primary', pageToken=page_token).execute()
            for event in events['items']:
                if 'end' in event and 'dateTime' in event['end']:
                    end_dt = parser.parse(event['end']['dateTime'])
                    end_dt_utc = end_dt.astimezone(pytz.utc)
                    end_time = end_dt_utc.timestamp()

                if 'start' in event and 'dateTime' in event['start']:
                    start_dt = parser.parse(event['start']['dateTime'])
                    start_dt_utc = start_dt.astimezone(pytz.utc)
                    start_time = start_dt_utc.timestamp()

                if 'attendees' in event and event['attendees']:
                    attendee_list = [item['email'] for item in event['attendees']]

                if 'summary' in event and event['summary']:
                    summary = event['summary']

                if 'location' in event and event['location']:
                    location = event['location']

                if 'description' in event and event['description']:
                    description = event['description']

                calendar = Calendar(summary=summary, location=location, description=description,
                        start_time=start_time, end_time=end_time, attendees=attendee_list)

                calendar_list_obj.calendar_list.append(calendar)
            page_token = events.get('nextPageToken')
            if not page_token:
                break

        return calendar_list_obj


    @staticmethod
    def _list(ctx: DataNodeContext) -> DataInterface:
        #TODO: implement me, this is where connects to a datasource, could be a database or a service
        raise NotImplementedError

    @staticmethod
    def _previous(ctx: DataNodeContext) -> DataInterface:
        return ctx.get_reference_context(ctx.source_index)


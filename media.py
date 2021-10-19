import os, requests, json
from datetime import datetime, timezone, timedelta

MEDIA_EVENTS_API = os.environ["MEDIA_EVENTS_API"]
ACCOUNT_NUMBER = os.environ["ACCOUNT_NUMBER"]

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S+00:00"

def getMediaEvents(auth_token: str):
  datetime_str = get_now_datetime_str()
  events_url = MEDIA_EVENTS_API.format(ACCOUNT_NUMBER=ACCOUNT_NUMBER, DATETIME_SINCE=datetime_str)
  headers={"TOKEN-AUTH": auth_token}
  response = requests.get(events_url, headers=headers)

  if (response.status_code != 200):
    print (f"Could not get media events: {response.status_code}. {response.text}")
    return None

  # get the response and extract the media metadata
  responseDict: dict = json.loads(response.text)
  media_metadata = responseDict["media"]
  if (not media_metadata):
    print (f"Response for media events did not contain metadata: {response.text}")

  # collect event creation times as datetime objects
  events_creation_times = []
  for event in media_metadata:
    if (not event.get("created_at")):
      continue
    event_time_obj = get_datetime_obj(event["created_at"])
    events_creation_times.append(event_time_obj)

  return events_creation_times

def get_now_datetime_str():
  # 2020-08-03T16:50:24+00:00
  now = datetime.now(timezone.utc)
  
  #TODO: testing... remove later
  # need to get last 10 minutes? needs to be planned and configurable
  now = now - timedelta(hours=12)

  return now.strftime(DATETIME_FORMAT)

def get_datetime_obj(datetimeStr: str):
  return datetime.strptime(datetimeStr, DATETIME_FORMAT)
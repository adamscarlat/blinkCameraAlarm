import os, requests, json, logging
from datetime import datetime, timezone, timedelta
from dateutil import tz

logger = logging.getLogger('alarm_logger')

MEDIA_EVENTS_API = os.environ["MEDIA_EVENTS_API"]
ACCOUNT_NUMBER = os.environ["ACCOUNT_NUMBER"]
EVENTS_LOOKBACK_MINUTES = int(os.environ["EVENTS_LOOKBACK_MINUTES"])

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S+00:00"

def get_media_events(auth_token: str):
  datetime_str = get_now_utc_datetime_str()
  events_url = MEDIA_EVENTS_API.format(ACCOUNT_NUMBER=ACCOUNT_NUMBER, DATETIME_SINCE=datetime_str)
  headers={"TOKEN-AUTH": auth_token}
  response = requests.get(events_url, headers=headers)

  if (response.status_code != 200):
    logger.error(f"Could not get media events: {response.status_code}. {response.text}")
    return None

  # get the response and extract the media metadata
  response_dict: dict = json.loads(response.text)
  media_metadata = response_dict["media"]
  if (not media_metadata):
    logger.info(f"Response for media events did not contain metadata: {response.text}")
    return []

  logger.info(f"Found {len(media_metadata)} events in given timespan")
  # collect event creation times as datetime objects
  events_creation_times = []
  for event in media_metadata:
    if (not event.get("created_at")):
      continue
    event_time_obj = get_utc_datetime_obj(event["created_at"])
    events_creation_times.append(event_time_obj)

  return events_creation_times

def get_now_utc_datetime_str():
  # 2020-08-03T16:50:24+00:00
  now = datetime.now(timezone.utc)
  now = now - timedelta(minutes=EVENTS_LOOKBACK_MINUTES)

  return now.strftime(DATETIME_FORMAT)

def get_utc_datetime_obj(datetimeStr: str):
  datetime_obj = datetime.strptime(datetimeStr, DATETIME_FORMAT)
  datetime_obj = datetime_obj.replace(tzinfo=tz.UTC)

  return datetime_obj
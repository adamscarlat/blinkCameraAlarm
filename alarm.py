from datetime import datetime, timedelta, timezone
from media import DATETIME_FORMAT

import os

ALARM_LOOKBACK_MINUTES = int(os.environ["ALARM_LOOKBACK_MINUTES"])
ALARM_THRESHOLD_EVENT_COUNT = int(os.environ["ALARM_THRESHOLD_EVENT_COUNT"])

'''
  Checks if there are a specific number of events in events_creation_times that fall into
  the alarm lookback period. See alarm specs in README for full details.
'''
def is_in_alarm(events_creation_times):
  alarm_lookback_end = datetime.now(timezone.utc)
  alarm_lookback_start = alarm_lookback_end - timedelta(minutes=ALARM_LOOKBACK_MINUTES)

  # instrumentation
  print (f"range start: {alarm_lookback_start.strftime(DATETIME_FORMAT)}")
  print (f"range end: {alarm_lookback_end.strftime(DATETIME_FORMAT)}")
  print ("-------------------------------------------------")

  events_in_range: int = 0
  is_in_alarm: bool = False
  for event_time in events_creation_times:
    if (is_in_datetime_range(alarm_lookback_start, alarm_lookback_end, event_time)):
      events_in_range += 1

    # instrumentation
    print (f"event: {event_time.strftime(DATETIME_FORMAT)}")
    print (f"events in range: {events_in_range}")

    if (events_in_range >= ALARM_THRESHOLD_EVENT_COUNT):
      is_in_alarm = True
      break
  
  return is_in_alarm

def is_in_datetime_range(range_start:datetime, range_end: datetime, event_time: datetime):
  # range start and end not crossing midnight
  if range_start < range_end:
    return event_time >= range_start and event_time <= range_end
  # crossing midnight (end after midnight, start before)
  else:
    return event_time >= range_start or event_time <= range_end
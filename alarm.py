from datetime import datetime, timedelta, timezone
from typing import List
import os, logging, time, subprocess

logger = logging.getLogger('alarm_logger')

ALARM_LOOKBACK_MINUTES = int(os.environ["ALARM_LOOKBACK_MINUTES"])
ALARM_THRESHOLD_EVENT_COUNT = int(os.environ["ALARM_THRESHOLD_EVENT_COUNT"])
ALARM_CYCLES_TOTAL = int(os.environ["ALARM_CYCLES_TOTAL"])
ALARM_CYCLE_TIME_SECONDS = int(os.environ["ALARM_CYCLE_TIME_SECONDS"])
ALARM_BETWEEN_CYCLES_PAUSE_SECONDS = 2

'''
  Checks if there are a specific number of events in events_creation_times that fall into
  the alarm lookback period. See alarm specs in README for full details.
'''
def is_in_alarm(events_creation_times: List[datetime]):
  alarm_lookback_end = datetime.now(timezone.utc)
  alarm_lookback_start = alarm_lookback_end - timedelta(minutes=ALARM_LOOKBACK_MINUTES)

  events_in_range: int = 0
  is_in_alarm: bool = False

  logger.info(f"Looking for events in alarm threshold")
  for event_time in events_creation_times:
    if (is_in_datetime_range(alarm_lookback_start, alarm_lookback_end, event_time)):
      events_in_range += 1
      logger.info(f"Found {events_in_range} events in alarm threshold. Event time: {str(event_time)}")

    if (events_in_range >= ALARM_THRESHOLD_EVENT_COUNT):
      is_in_alarm = True
      break
  
  logger.info(f"Events found: {events_in_range}. Alarm threshold: {ALARM_THRESHOLD_EVENT_COUNT}. is in alarm: {is_in_alarm}")
  return is_in_alarm

def run_alarm():
  alarm_cycle_count = 1

  while alarm_cycle_count <= ALARM_CYCLES_TOTAL:
    logger.info(f"Alarm is on. Cycle: {alarm_cycle_count}/{ALARM_CYCLES_TOTAL}")
    run_alarm_cycle()
    
    time.sleep(ALARM_BETWEEN_CYCLES_PAUSE_SECONDS)
    alarm_cycle_count += 1

  logger.info(f"Alarm is off. Ran for {alarm_cycle_count}, {ALARM_CYCLE_TIME_SECONDS} each. \
      Total time in alarm: \
      {(ALARM_CYCLE_TIME_SECONDS + ALARM_BETWEEN_CYCLES_PAUSE_SECONDS) * alarm_cycle_count} seconds")

def run_alarm_cycle():
  for _ in range(ALARM_CYCLE_TIME_SECONDS):
    subprocess.run(["bash", "scripts/usb_on.sh"], capture_output=True)
    time.sleep(0.5)

    subprocess.run(["bash", "scripts/usb_off.sh"], capture_output=True) 
    time.sleep(0.5)

def is_in_datetime_range(range_start:datetime, range_end: datetime, event_time: datetime):
  # range start and end not crossing midnight
  if range_start < range_end:
    return event_time >= range_start and event_time <= range_end
  # crossing midnight (end after midnight, start before)
  else:
    return event_time >= range_start or event_time <= range_end


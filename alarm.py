from datetime import datetime, timedelta, timezone
from typing import List
import os, logging, time, subprocess, inspect

logger = logging.getLogger('alarm_logger')

ALARM_LOOKBACK_MINUTES = int(os.environ["ALARM_LOOKBACK_MINUTES"])
ALARM_THRESHOLD_EVENT_COUNT = int(os.environ["ALARM_THRESHOLD_EVENT_COUNT"])
ALARM_CYCLES_TOTAL = int(os.environ["ALARM_CYCLES_TOTAL"])
ALARM_CYCLE_TIME_SECONDS = int(os.environ["ALARM_CYCLE_TIME_SECONDS"])
ALARM_BETWEEN_CYCLES_PAUSE_SECONDS = 2

# get path to app root
full_module_path = inspect.getfile(inspect.currentframe())
CWD = '/'.join(full_module_path.split('/')[:-1])

# assumes that scripts are a child folder to this module
ALARM_ON_SCRIPT = f"{CWD}/scripts/usb_on.sh"
ALARM_OFF_SCRIPT = f"{CWD}/scripts/usb_off.sh"

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

'''
  Runs {ALARM_CYCLES_TOTAL} alarm cycles with {ALARM_BETWEEN_CYCLES_PAUSE_SECONDS} pause in between
  each cycle.
'''
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

'''
  Does an ON then OFF with a pause of 0.5 seconds. Repeats this for {ALARM_CYCLE_TIME_SECONDS}
  seconds.
'''
def run_alarm_cycle():
  for _ in range(ALARM_CYCLE_TIME_SECONDS):
    sub_proc_control(ALARM_ON_SCRIPT, "ON")
    time.sleep(0.5)

    sub_proc_control(ALARM_OFF_SCRIPT, "OFF")
    time.sleep(0.5)

'''
  Given an absolute path for a script, runs it as a subprocess. If the subprocess returns a non 0 exit
  code, this function will raise an IOError.
'''
def sub_proc_control(script_path: str, mode_str: str):
  sp_status = subprocess.run(["bash", script_path], capture_output=True, text=True)
  if (sp_status.returncode != 0):
    logger.error(f"Non 0 exit code in ALARM {mode_str} sub process. Exit code: {sp_status.returncode}. Message: {sp_status.stderr}")
    raise IOError("HARDWARE CONTROL FAILURE! Aborting alarm cycle")
  
def is_in_datetime_range(range_start:datetime, range_end: datetime, event_time: datetime):
  # range start and end not crossing midnight
  if range_start < range_end:
    return event_time >= range_start and event_time <= range_end
  # crossing midnight (end after midnight, start before)
  else:
    return event_time >= range_start or event_time <= range_end


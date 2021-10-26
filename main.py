import os, time, sys, logging
from logging import handlers
from alarm import is_in_alarm, run_alarm

from auth import get_auth_token
from media import get_media_events

logger = logging.getLogger('alarm_logger')

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
UNIQUE_LOGIN_ID = os.environ["UNIQUE_LOGIN_ID"]
SLEEP_TIME_SECONDS = int(os.environ["SLEEP_TIME_SECONDS"])
ERROR_RETRY_LIMIT = int(os.environ["ERROR_RETRY_LIMIT"])
MAX_LOG_SIZE_MB = int(os.environ["MAX_LOG_SIZE_MB"])
LOG_PATH = os.environ["LOG_PATH"]

def run():
  while True:
    # get auth token
    auth_token = get_auth_token(EMAIL, PASSWORD, UNIQUE_LOGIN_ID)
    if (not auth_token):
      logger.error("Encountered issues during login. Aborting...")

    # get media events
    events_creation_times = get_media_events(auth_token)

    should_sound_alarm = False
    if (events_creation_times):
      # analyze media events
      should_sound_alarm = is_in_alarm(events_creation_times)

    # if alarm, activate usb module
    if (should_sound_alarm):
      run_alarm()
    else:
      logger.debug("No alarm")

    # pause
    time.sleep(SLEEP_TIME_SECONDS)

def run_wrapper(current_iteration=1):
  try:
    run()
  except Exception as ex:
    if (current_iteration > ERROR_RETRY_LIMIT):
      logger.fatal(f"Current iteration: {current_iteration} exceeded max: {ERROR_RETRY_LIMIT}")
      sys.exit("Could not recover from error. Stopping program...")

    ex_msg = f'''\
    Moudle run into an unexcpected error. Will retry with exponential 
    backoff. Details:
      Exception type: {type(ex)}.
      Exception: {ex}
    Pausing for {2**current_iteration} seconds...
    '''
    logger.exception(ex_msg)

    # sleep and retry
    time.sleep(2**current_iteration)
    run_wrapper(current_iteration+1)

def set_logging():
  global logger
  
  msg_format = '%(asctime)s:%(levelname)s:%(funcName)s():%(lineno)s:%(message)s'
  date_format='%Y-%m-%d %H:%M:%S'
  max_log_size_bytes = 1024 * 1024 * MAX_LOG_SIZE_MB

  # create log directory if not exist
  os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

  log_formatter = logging.Formatter(fmt=msg_format, datefmt=date_format)
  log_handler = handlers.RotatingFileHandler(LOG_PATH, maxBytes=max_log_size_bytes, backupCount=7)
  log_handler.setFormatter(log_formatter)

  logger.setLevel(logging.INFO)
  logger.addHandler(log_handler)
  

if __name__ == "__main__":
  set_logging()
  run_wrapper()

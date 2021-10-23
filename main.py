import os, time, sys
from datetime import datetime, timezone
from alarm import is_in_alarm

from auth import get_auth_token
from media import get_media_events

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
UNIQUE_LOGIN_ID = os.environ["UNIQUE_LOGIN_ID"]
SLEEP_TIME_SECONDS = int(os.environ["SLEEP_TIME_SECONDS"])
ERROR_RETRY_LIMIT = int(os.environ["ERROR_RETRY_LIMIT"])

def run():
  while True:
    # get auth token
    auth_token = get_auth_token(EMAIL, PASSWORD, UNIQUE_LOGIN_ID)
    if (not auth_token):
      print ("Encountered issues during login. Aborting...")

    # get media events
    events_creation_times = get_media_events(auth_token)

    should_sound_alarm = False
    if (events_creation_times):
      # analyze media events
      should_sound_alarm = is_in_alarm(events_creation_times)

    # if alarm, activate usb module
    if (should_sound_alarm):
      print ("TODO: run usb module")
    else:
      print ("no alarm")

    # pause
    time.sleep(SLEEP_TIME_SECONDS)

def run_wrapper(current_iteration=1):
  try:
    run()
  # TODO: once logging module is used, it will print the stack trace. need to verify
  except Exception as ex:
    if (current_iteration > ERROR_RETRY_LIMIT):
      sys.exit("Could not recover from error. Stopping program...")

    ex_msg = f'''\
    --------------------------------------------------------------------
    Moudle run into an unexcpected error. Will retry with exponential 
    backoff. Details:
      Exception type: {type(ex)}.
      Exception: {ex}
    Pausing for {2**current_iteration} seconds...
    --------------------------------------------------------------------
    '''
    print (ex_msg)

    # sleep and retry
    time.sleep(2**current_iteration)
    run_wrapper(current_iteration+1)

if __name__ == "__main__":
  run_wrapper()

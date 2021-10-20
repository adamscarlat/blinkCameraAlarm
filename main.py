import os
from datetime import datetime, timezone
from alarm import is_in_alarm

from auth import login
from media import get_media_events

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
UNIQUE_LOGIN_ID = os.environ["UNIQUE_LOGIN_ID"]

auth_token = login(EMAIL, PASSWORD, UNIQUE_LOGIN_ID)
if (not auth_token):
  print ("Encountered issues during login. Aborting...")

events_creation_times = get_media_events(auth_token)
if (not events_creation_times):
  now = datetime.now()
  now_str = now.strftime()
  print (f"{now_str} - No events found")

should_sound_alarm = is_in_alarm(events_creation_times)

print (f"Should sound alarm: {should_sound_alarm}")
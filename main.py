import os

from auth import login
from media import getMediaEvents

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
UNIQUE_LOGIN_ID = os.environ["UNIQUE_LOGIN_ID"]

auth_token = login(EMAIL, PASSWORD, UNIQUE_LOGIN_ID)
if (not auth_token):
  print ("Encountered issues during login. Aborting...")

getMediaEvents(auth_token)
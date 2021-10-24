import os, requests, json, logging
from datetime import datetime, timedelta

logger = logging.getLogger('alarm_logger')

LOGIN_API = os.environ["LOGIN_API"]
REAUTH_TIME_MINUTES = int(os.environ["REAUTH_TIME_MINUTES"])

last_login_time = datetime.min
cached_token = None

def get_auth_token(email: str, password: str, unique_login_id: str):
  global cached_token, last_login_time
  
  # only do a login if cached token is older than {REAUTH_TIME_MINUTES}
  now = datetime.now()
  if (now - last_login_time >= timedelta(minutes=REAUTH_TIME_MINUTES) or not cached_token):
    logger.info(f"Renewing cached token. Current time: {str(now)}. Last login: {str(last_login_time)}")
    cached_token = login(email, password, unique_login_id)
    last_login_time = now
  
  return cached_token

# returns auth token
def login(email: str, password: str, unique_login_id: str) -> str:
  headers = {'Content-Type': 'application/json'}
  
  # reauth and unique_id are to prevent MFA during login
  jsonBody = json.dumps({
    "email":email, 
    "password":password, 
    "reauth": True,
    "unique_id":unique_login_id
  })
  response = requests.post(LOGIN_API, headers=headers, data=jsonBody)

  if (response.status_code != 200):
    logger.error(f"Could not login: {response.status_code}. {response.text}")
    return None

  response_dict: dict = json.loads(response.text)

  if (not response_dict.get("auth") or not response_dict["auth"].get("token")):
    logger.error(f"Did not find auth token in response")
    return None
  
  logger.info("Authentication was successful. Passing auth token downstream")
  return response_dict["auth"]["token"]

  
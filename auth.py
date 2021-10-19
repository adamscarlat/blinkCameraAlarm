import os, requests, json

LOGIN_API = os.environ["LOGIN_API"]

# returns auth token
def login(email: str, password: str, unique_login_id: str) -> str:
  headers = {'Content-Type': 'application/json'}
  jsonBody = json.dumps({
    "email":email, 
    "password":password, 
    "reauth": True,
    "unique_id":unique_login_id
  })
  response = requests.post(LOGIN_API, headers=headers, data=jsonBody)

  if (response.status_code != 200):
    print (f"Could not login: {response.status_code}. {response.text}")
    return None

  responseDict: dict = json.loads(response.text)

  if (not responseDict.get("auth") or not responseDict["auth"].get("token")):
    print (f"Did not find auth token in response")
    return None
  
  return responseDict["auth"]["token"]

  
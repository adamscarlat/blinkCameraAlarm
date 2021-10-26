APP_ROOT=/home/pi/blinkCameraAlarm
PYTHON3_PATH=/usr/bin/python3

# set the environment variables
export $(xargs <${APP_ROOT}/vars.env)
export $(xargs <${APP_ROOT}/credentials.env)

# run the app
${PYTHON3_PATH} ${APP_ROOT}/main.py

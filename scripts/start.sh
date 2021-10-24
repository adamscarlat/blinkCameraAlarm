APP_ROOT=/home/pi/blinkCameraAlarm
PYTHON3_PATH=/usr/bin/python3

# set the environment variables
export $(xargs <${APP_ROOT}/.env)

# start with USB power off
bash ${APP_ROOT}/scripts/usb_off.sh

# run the app
${PYTHON3_PATH} ${APP_ROOT}/main.py

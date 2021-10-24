# set the environment variables
export $(xargs <.env)

# run the app
/usr/bin/python3 /home/pi/blinkCameraAlarm/main.py

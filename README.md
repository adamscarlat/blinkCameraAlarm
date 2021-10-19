# blinkCameraAlarm

Alarm that is triggered based on camera events

# TODO

- POC:

  - make sure that the auth token does not require 2FA.
  - check media events API update speed after a video is made.
  - RPI: need to make sure it's working and that the usb port allows power supply changes via code.
  - lamp: get the lamp and tie it all together

- Add logging (using the logging library):

  - log to s3 (or any location that's easy to access)?

- harden with try/catch

- Create a systemd service:
  - need a bash script for the service to read the .env file into the environment
    and start the program

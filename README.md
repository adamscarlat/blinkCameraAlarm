# blinkCameraAlarm

Alarm that is triggered based on camera events

## Setup

This alarm system is configured to work on Debian based systems. It requires Python >= 3.8.

To set up the system:

- Clone the repository:

`git clone https://github.com/adamscarlat/blinkCameraAlarm`

- Create a `credentials.env` file with your Blink system credentials. File should have the
  following:

```
# blink creds
EMAIL=*****
PASSWORD=*****
UNIQUE_LOGIN_ID=<RANDOM_UUID>
ACCOUNT_NUMBER==*****

# twillo creds
TWILLO_FROM_NUMBER=******
TWILLO_TO_NUMBER=*******
TWILLO_ACCOUNT=******
TWILLO_SECRET=*******
```

- From the repo root folder, run the set up script:

`bash ./scripts/setup.sh`

- Check that the service is running:

`systemctl status alarm.service`

- Check that the logs are saving:

`cat {LOG_PATH}`

## Alarm Specs

Alarm will receive a list of events creation times in the time period of `{ALARM_LOOKBACK_MINUTES}`.

Alarm will take the current time, `{now}` (which should be sufficiently close to the end of the `ALARM_LOOKBACK_MINUTES` period),
and count the number of events creation times that are within range of `{now} - {ALARM_LOOKBACK_MINUTES}`.

If there are more or equal number of events than `{ALARM_THRESHOLD_EVENT_COUNT}`, alarm will sound.

## Examples

In the below examples, the parameters are as follows:

- `ALARM_LOOKBACK_MINUTES` = 2
- `ALARM_THRESHOLD_EVENT_COUNT` = 2

- `E1 --> E2` = time period of ALARM_LOOKBACK_MINUTES
- `e1...en` = events captured in above period

**Scenario 1** - alarm will not sound since there is only one event in ALARM_LOOKBACK_MINUTES
and it's less than ALARM_THRESHOLD_EVENT_COUNT

```

          E1 >--e1-------------> E2
  >--------------------------------------->
```

**Scenario 2** - alarm will sound

```
          E1 >--e1--e2---e3-e4-> E2
  >--------------------------------------->
```

# TODO

- POC:
  !!! Clean up lamp stuff (usb, alarm cycle code) and document new twillo call workflow (credentials)
  !!! clean up twillo code (env vars, etc...)

  - see about twillo calls API
  - adjust subsequent calls pause time

  - (DONE) make sure that the auth token does not require 2FA.
  - (DONE) check media events API update speed after a video is made.
    - events are registered after the video (shorter videos with short debouce time will be better for this)
  - (DONE) move secrets out of .env to a non-tracked file and track .env. Will need to read them into environment

- Add logging (using the logging library)

  - (DONE) show time
  - (DONE) show function name
  - (DONE) rotate log files
  - log to s3 (or any location that's easy to access)?

- harden with try/catch

  - (DONE) add try/catch on main loop with exponential backoff

- Create a systemd service:

  - (DONE) need a bash script for the service to read the .env file into the environment
    and start the program
  - (DONR) create set up script (to set up the service with systemd).
  - (DONE) create teardown script for systemd
  - (DONE) configure systemd service for limited retries with pause in between

- Add a system scheduler to turn WHOLE system on and off at certain times

# blinkCameraAlarm

Alarm that is triggered based on camera events

## Alarm Specs

Alarm will receive a list of events creation times in the time period of `{EVENTS_LOOKBACK_MINUTES}`.

Alarm will take the current time, `{now}` (which should be sufficiently close to the end of the `EVENTS_LOOKBACK_MINUTES` period),
and count the number of events creation times that are within range of `{now} - {ALARM_LOOKBACK_MINUTES}`.

If there are more or equal number of events than `{ALARM_THRESHOLD_EVENT_COUNT}`, alarm will sound.

## Examples

In the below examples, the parameters are as follows:

- `EVENTS_LOOKBACK_MINUTES` = 3
- `ALARM_LOOKBACK_MINUTES` = 2
- `ALARM_THRESHOLD_EVENT_COUNT` = 2

- `E1 --> E2` = time period of EVENTS_LOOKBACK_MINUTES
- `e1...en` = events captured in above period
- `A1 --> A2` = time period of ALARM_LOOKBACK_MINUTES

**Scenario 1** - alarm will not sound since there is only one event in ALARM_LOOKBACK_MINUTES
and it's less than ALARM_THRESHOLD_EVENT_COUNT

```

          E1 >--e1--e2-----e3--> E2
  >--------------------------------------->
                      A1 >-----> A2
```

**Scenario 2** - alarm will sound

```
          E1 >--e1--e2---e3-e4-> E2
  >--------------------------------------->
                      A1 >-----> A2
```

# TODO

- POC:

  - (DONE) make sure that the auth token does not require 2FA.
  - check media events API update speed after a video is made.
  - RPI: need to make sure it's working and that the usb port allows power supply changes via code.
  - lamp: get the lamp and tie it all together

- Add logging (using the logging library):

  - log to s3 (or any location that's easy to access)?

- harden with try/catch

  - (DONE) add try/catch on main loop with exponential backoff

- Create a systemd service:
  - need a bash script for the service to read the .env file into the environment
    and start the program

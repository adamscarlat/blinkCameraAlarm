# create, enable and start service
sudo cp ./scripts/alarm.service /lib/systemd/system/alarm.service
sudo systemctl daemon-reload
sudo systemctl enable alarm.service
sudo systemctl start alarm.service
if [ ! -f ./credentials.txt ]
then
  echo "Cannot start without credentials. See readme for more details"
  exit 1
fi

# install dependencies
pip3 install -r requirements.txt

# create, enable and start service
sudo cp ./scripts/alarm.service /lib/systemd/system/alarm.service
sudo systemctl daemon-reload
sudo systemctl enable alarm.service
sudo systemctl start alarm.service
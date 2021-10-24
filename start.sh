# set the environment variables
export $(xargs <.env)

# run the app
/usr/bin/python3 main.py

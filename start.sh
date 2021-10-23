# set the environment variables
export $(xargs <.env)

# run the app
python main.py

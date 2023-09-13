# JobScanner

Web Scraping for notification of freelance jobs on mql5.com

- Clone the repository ```git clone https://github.com/paulovisam/JobScanner-MQL5.git```

## Preparing Environment
- Open cmd as administrator and go to the folder directory
- Create a virtual environment ```python3 -m venv venv```
- Activate the virtual environment ```cd venv/Scripts/activate.bat``` in PowerShell ```& "venv/Scripts/Activate.ps1"``` linux ```source venv/bin/activate```
- Upgrade pip ```python3 -m pip install --upgrade pip```
- Install the packages ```pip install -r requirements.txt```
- Create a .env file
- Add variables
```
LOGIN=value_login
PASSWORD=value_password
TOKEN=telegram_bot_token
TIMER_SECONDS=sweep_frequency
CHAT_ID=your_chat_id
COUNTRY=en
```
If it is the first time:
- Go to the src directory ```cd src```
- Run the command ```alembic upgrade head```

Run with ```python3 main.py``` in the project root

## Docker
Run ```docker compose up -d```

Or if you prefer:
```
docker build -f Dockerfile -t jobscanner_img .
docker run --env-file .env -it jobscanner_img
```
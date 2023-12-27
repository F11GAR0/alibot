# ALIBOT
## Run steps

#### OS Requierements
| Requierement | Version |
|---|-----|
| python | >= 3.8.2 |
| docker-ce | >= 4:20.10.24-1 |
| docker-ce-cli | >= 1:20.10.24-1 |
| nss (libnss) | >= 3.79 |
| gconf2 (libgconf) | >= 3.2.6-21 |
| fontconfig | >= fontconfig-2.14.2-2 |

#### 1. Create virtual environment
Linux / Windows / macOS:
```sh
python -m venv venv
```
#### 2. Activate virual environment
Linux:
```sh
source venv/bin/activate
```
Windows:
```sh
# In cmd.exe
venv\Scripts\activate.bat
# In PowerShell
venv\Scripts\Activate.ps1
```
#### 3. Install requirements
```sh
pip install -r requirements.txt
```
##### 3.1 Install selenium chromedriver if you dont want to use docker
You can download it from https://chromedriver.chromium.org/downloads.
Put it in this directory ( *alibot/chromedriver* )
#### 4. Setup docker environments
```sh
docker pull selenium/standalone-chrome
```
#### 5. Run bot (no docker)
```sh
python main.py
```
#### 6. Run bot (docker)
```sh
docker-compose -f "docker-compose.yml" down
docker-compose -f "docker-compose.yml" up -d --build
docker exec -d alibot-dev python3 /debugpy/launcher 172.17.0.1:54775 -- main.py
```

## Config file

*config.py*
```sh
TG_BOT_TOKEN = "" # telegram bot token from bot father
DOCKER = True # True - if you want to use docker, False - if not
SQLALCHEMY_DATABASE_URI = 'sqlite:////alidb/' # path to database
```
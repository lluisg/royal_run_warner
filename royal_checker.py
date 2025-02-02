import os
import time
import requests
import json
import traceback

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pushbullet import Pushbullet

def check_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if "Der findes ingen billetter til salg" in soup.get_text():
        # "Tickets are sold out"
        return False
    else:
        # "Tickets are available"
        return True

def send_pushbullet(PB, text=None, url=None, failed=False):
    if not failed:
        PB.push_link('New ticket on sale:', url, text, channel=PB.channels[0])
    else:
        PB.push_note('The Royal Run script failed', 'It failed ...', channel=PB.channels[0])

def main():
    SLEEP_TIME = 180 # time to sleep between runs in seconds, 3m
    SLEEP_ON_FOUND = 90 # extra time to sleep if found
    URL = 'https://www.sportstiming.dk/event/15228/resale?distance=85498' # 5km run link
    LOG_FILE = './logs_messages.json'

    try:
        # Load parameters from the .env file
        load_dotenv()
        pushbullet_token = os.getenv('PB_API')

        pb = Pushbullet(pushbullet_token)

        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as file:
                output = json.load(file)
        else:
            output = {}

        while True:
            result = check_website(URL)
            date = time.strftime("%Y-%m-%d %H:%M:%S")
            output[str(date)] = str(result)

            with open(LOG_FILE, 'w') as f:
                json.dump(output, f, indent=4)

            if result:
                message = f"Royal run ticket on sale!"
                send_pushbullet(pb, message, url=URL, failed=False)
                print('Saaale!!!! on', date)
                time.sleep(SLEEP_ON_FOUND)

            time.sleep(SLEEP_TIME)

    except KeyboardInterrupt:
        print("Script stopped by user.")

    except Exception as e:
        print('Failed')
        traceback.print_exc()
        # Will try to send a notification that the script is down
        send_pushbullet(pb, failed=True)


if __name__ == "__main__":
    load_dotenv()
    main()

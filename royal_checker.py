import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time
from pushbullet import Pushbullet
import json

def check_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if "Der findes ingen billetter til salg" in soup.get_text():
        # "Tickets are sold out"
        return False
    else:
        # "Tickets are available"
        return True

def send_notification(title, body):
    API_KEY = os.getenv("API_KEY")
    pb = Pushbullet(API_KEY)
    push = pb.push_note(title, body)

def main():
    TIME = 20
    URL = 'https://www.sportstiming.dk/event/13416/resale'
    FILENAME = 'C:/Users/Lluis/Desktop/Projects/royal_run_warner/logs_outputs.json'

    try:
        if os.path.exists(FILENAME):
            with open(FILENAME, 'r') as file:
                output = json.load(file)
        else:
            output = {}

        while True:
            result = check_website(URL)
            date = time.strftime("%Y-%m-%d %H:%M:%S")
            output[str(date)] = str(result)

            if result:
                event_title = "On sale!"
                event_body = "Royal run on sale!"
                send_notification(event_title, event_body)
                print('Saaale!!!! on', date)
                time.sleep(70)
            else:
                print('.')

            with open(FILENAME, 'w') as f:
                json.dump(output, f, indent=4)

            time.sleep(TIME)

    except KeyboardInterrupt:
        print("Script stopped by user.")

if __name__ == "__main__":
    load_dotenv()
    main()

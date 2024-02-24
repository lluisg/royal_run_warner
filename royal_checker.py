import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time
from pushbullet import Pushbullet
import json

# Function to scrape the website and check for certain conditions
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
    print(API_KEY)
    pb = Pushbullet(API_KEY)
    push = pb.push_note(title, body)

# Main function to check website and send notification every 30 seconds
def main():
    TIME = 10
    URL = 'https://www.sportstiming.dk/event/13416/resale'
    FILENAME = 'log_output.json'

    try:
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
            else:
                print('.')

            time.sleep(TIME)  # Sleep for 30 seconds before checking again

            with open(FILENAME, 'w') as f:
                # Write the list to the file in JSON format
                json.dump(output, f, indent=4)

    except KeyboardInterrupt:
        print("Script stopped by user.")

if __name__ == "__main__":
    load_dotenv()
    main()

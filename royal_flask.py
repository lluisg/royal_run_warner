from flask import Flask
from bs4 import BeautifulSoup
import requests
import yagmail
from dotenv import load_dotenv
import os
import threading
import time

app = Flask(__name__)

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

# Function to send email with the results
def send_email(subject, body):
    load_dotenv()
    MAIL_SENDER = "lluis.guardia.f@gmail.com"
    PASS_SENDER = os.getenv("MAIL_PASSWORD")
    receiver = "lluis.guardia.f@gmail.com"
    yag = yagmail.SMTP(MAIL_SENDER, PASS_SENDER)
    yag.send(
        to=receiver,
        subject=subject,
        contents=body,
    )

# Function to perform checking and emailing every 3 minutes
def check_and_email():
    while True:
        url5km = 'https://www.sportstiming.dk/event/13416/resale?distance=72951'
        url10km = 'https://www.sportstiming.dk/event/13416/resale?distance=72952'

        result5km = check_website(url5km)
        result10km = check_website(url10km)

        message = f'Tickets for 5km: {result5km}\nTickets for 10km: {result10km}'

        if result5km or result10km:
            send_email("Ticket For Sale", message)

        time.sleep(180)  # Sleep for 3 minutes before checking again

@app.route('/')
def index():
    return 'Flask app is running!'

if __name__ == '__main__':
    # Start the background thread
    bg_thread = threading.Thread(target=check_and_email)
    bg_thread.daemon = True
    bg_thread.start()

    # Run the Flask app
    app.run(debug=True)

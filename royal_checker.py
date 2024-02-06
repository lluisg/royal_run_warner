import requests
from bs4 import BeautifulSoup
import yagmail
from dotenv import load_dotenv
import os

# Function to scrape the website and check for certain conditions
def check_website(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  # print(soup.encode('utf-8'))
  return True
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

# Main function to check website and send email every 10 minutes
def main():
  url5km = 'https://www.sportstiming.dk/event/13416/resale?distance=72951'
  url10km = 'https://www.sportstiming.dk/event/13416/resale?distance=72952'

  result5km = check_website(url5km)
  result10km = check_website(url10km)
  print('5km:', result5km, ', 10km:', result10km)

  if result5km or result10km:
    send_email("Ticket For Sale", 'Tickets for 5km:'+str(result5km)+'\nTickets for 10km:'+str(result10km))

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup

import slack
import os
from pathlib import Path
from dotenv import load_dotenv

import time
import random

def main():
    url = 'https://www.bbc.com' #or input("URL: ")
    selector = 'a[rev="hero1|headline"]' #or input("Selector: ")

    while True:
        message = f"BBC Headline: {scrape(url, selector)}"
        send_to_slack(message)
        waitingTime = random.uniform(1*60, 10*60)
        time.sleep(waitingTime)
        print(f"Waited for {int(waitingTime/60)} minutes\n")

def scrape(url, selector):
    response = requests.get(url)

    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'lxml') #or 'html.parser'

    targets = soup.select(selector)

    for target in targets:
        print(target.text.strip())

    print()
    return targets[0].text.strip()

def send_to_slack(message):
    envPath = Path('.') / '.env'
    load_dotenv(dotenv_path=envPath)

    client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
    client.chat_postMessage(channel='#notify-me', text=message)

if __name__ == '__main__':
    main()

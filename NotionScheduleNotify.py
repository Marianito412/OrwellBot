from datetime import datetime
from notion.client import NotionClient
import requests
import pytz
import os

token = os.environ.get("TOKEN")
url = os.environ.get("NOTION_URL")

print(f"{token}\n{url}")
def sendMessage(msg, eventStart, eventEnd):
    BOT_API_KEY = os.environ.get("ORWELL_API")
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(BOT_API_KEY)

    msg = f"<b>{msg}</b>\n{eventStart}-{eventEnd}"

    requests.get(url, params={'chat_id':'1045229863','text': msg, 'parse_mode':'HTML'})

def isBetween(Start: str, End: str, format="%I:%M %p") -> bool:
    """This function returns true if the current time exists within the given times"""
    tz = pytz.timezone("America/Costa_Rica")
    now = datetime.now(tz)
    return (now.time() >= datetime.strptime(Start, format).time()) and (now.time() <= datetime.strptime(End, format).time())

def main():
    tz = pytz.timezone("America/Costa_Rica")
    now = datetime.now(tz)
    print(now.weekday(), now.day)

    isEarly = isBetween("07:00 AM", "08:00 PM")

    if (now.weekday() == 3) and  isEarly:
        sendMessage("New Free Game in Epic Games Store, Grab It", "", "")

    if (now.weekday() == 1 and now.day <=7) and isEarly:
        sendMessage("New Unreal Engine MarketPlace Content, Check It Out", "", "")

    client = NotionClient(token_v2=token)
    database = client.get_collection_view(url)

    for i in database.collection.get_rows():
        eventStart = i.Hours[0].split("→")[0].replace("md", "pm").upper()
        eventStart = datetime.strptime(eventStart, "%I:%M%p").time()

        eventEnd = i.Hours[-1].split("→")[-1].replace("md", "pm").upper()
        eventEnd = datetime.strptime(eventEnd, "%I:%M%p").time()
        print(f"{eventStart} - {eventEnd}")

        if (now.time()>=eventStart and now.time()<=eventEnd) and (now.strftime("%A") in i.Days):

            firstHour = [x.replace("md", "pm").upper() for x in Hours[0].split("→")]
            if isBetween(firstHour[0], firstHour[1], format="%I:%M%p"):
                sendMessage(i.name, eventStart.strftime("%I:%M %p"), eventEnd.strftime("%I:%M %p"))

if __name__ == "__main__":
    main()

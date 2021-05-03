from datetime import datetime
from notion.client import NotionClient
import requests
import os
    
token = os.environ.get("TOKEN")
url = os.environ.get("NOTION_URL")

print(f"{token}\n{url}")
def sendMessage(msg, eventStart, eventEnd):
    BOT_API_KEY = os.environ("ORWELL_API")
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(BOT_API_KEY)

    msg = f"<b>{msg}</b>\n{eventStart}-{eventEnd}"

    requests.get(url, params={'chat_id':'1045229863','text': msg, 'parse_mode':'HTML'})

def main():
    now = datetime.now()
    print(now.strftime("%A"))

    client = NotionClient(token_v2=token)
    database = client.get_collection_view(url)

    for i in database.collection.get_rows():
        eventStart = i.Hours[0].split("→")[0].replace("md", "pm").upper()
        eventStart = datetime.strptime(eventStart, "%I:%M%p").time()

        eventEnd = i.Hours[-1].split("→")[-1].replace("md", "pm").upper()
        eventEnd = datetime.strptime(eventEnd, "%I:%M%p").time()
        print(f"{eventStart} - {eventEnd}")

        if (now.time()>=eventStart and now.time()<=eventEnd) and (now.strftime("%A") in i.Days):
            sendMessage(i.name, eventStart.strftime("%I:%M %p"), eventEnd.strftime("%I:%M %p"))

if __name__ == "__main__":
    main()

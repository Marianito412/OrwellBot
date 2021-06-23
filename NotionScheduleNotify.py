from datetime import datetime
import requests, json
import pytz
import os

DEBUG = False

if DEBUG:
    import keys
    BOT_API_KEY = keys.orwellKey

    NotionKey = keys.NotionSecret
    databaseId = keys.NotionDatabaseId
else:
    BOT_API_KEY = os.environ.get("ORWELL_API")

    NotionKey = os.environ.get("NOTION_KEY")
    databaseId = os.environ.get("DATABASE_ID")

header = {
    "Authorization": f"Bearer {NotionKey}",
    "Notion-Version": "2021-05-13",
    "Content-Type": "application/json",
}

class event:
    Name = None
    Days = None
    Hours = None
    def __init__(self, package):
        self.Name = package["properties"]["Name"]["title"][0]["text"]["content"]
        self.Days = [Day["name"] for Day in package["properties"]["Days"]["multi_select"]]
        self.Hours = [Hour["name"] for Hour in package["properties"]["Hours"]["multi_select"]]


def sendMessage(msg, eventStart, eventEnd):
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(BOT_API_KEY)
    msg = f"<b>{msg}</b>\n{eventStart}-{eventEnd}"

    requests.get(url, params={'chat_id':'1045229863','text': msg, 'parse_mode':'HTML'})

def getSchedule(databaseId, headers):
    url = f"https://api.notion.com/v1/databases/{databaseId}/query"

    return requests.request("POST", url, headers=headers).json()

def isBetween(Start: str, End: str, format="%I:%M %p") -> bool:
    """This function returns true if the current time exists within the given times"""
    tz = pytz.timezone("America/Costa_Rica")
    now = datetime.now(tz)
    return (now.time() >= datetime.strptime(Start, format).time()) and (now.time() <= datetime.strptime(End, format).time())

def main():
    tz = pytz.timezone("America/Costa_Rica")
    now = datetime.now(tz)

    isEarly = isBetween("07:00 AM", "08:00 AM")

    if (now.weekday() == 3) and  isEarly:
        sendMessage("New Free Game in Epic Games Store, Grab It", "", "")

    if (now.weekday() == 1 and now.day <=7) and isEarly:
        sendMessage("New Unreal Engine MarketPlace Content, Check It Out", "", "")

    events = [event(item) for item in getSchedule(databaseId, header).get("results")]

    for i in events:
        eventStart = i.Hours[0].split("→")[0].replace("md", "pm").upper()
        eventStart = datetime.strptime(eventStart, "%I:%M%p").time()

        eventEnd = i.Hours[-1].split("→")[-1].replace("md", "pm").upper()
        eventEnd = datetime.strptime(eventEnd, "%I:%M%p").time()
        print(f"{eventStart} - {eventEnd}")

        if (now.time()>=eventStart and now.time()<=eventEnd) and (now.strftime("%A") in i.Days):

            firstHour = [x.replace("md", "pm").upper() for x in i.Hours[0].split("→")]
            if isBetween(firstHour[0], firstHour[-1], format="%I:%M%p"):
                sendMessage(i.Name, eventStart.strftime("%I:%M %p"), eventEnd.strftime("%I:%M %p"))

if __name__ == "__main__":
    main()
    #with open("test.json", "w", encoding="utf-8") as f:
    #    json.dump(getSchedule(databaseId, header), f, ensure_ascii=False)

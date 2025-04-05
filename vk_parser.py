from playwright.sync_api import sync_playwright
import json
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

url = "https://vkvideo.ru/playlist/-202211208_8"

dictionary = {
    "Лейкерс":"LAL",
    "Новый Орлеан":"NOP",
    "Клипперс":"LAC",
    "Даллас":"DAL",
    "Голден Стэйт":"GSW",
    "Сан-Антонио":"SAS",
    "Кливленд":"CLE",
    "Хьюстон":"HOU",
    "Оклахома":"OKC",
    "Чикаго":"CHI",
    "Портленд":"POR",
    "Торонто":"TOR",
    "Детройт":"DET",
    "Бостон":"BOS",
    "Финикс": "PHX",
    "Индиана":"IND",
    "Юта":"UTA",
    "Шарлотт":"CHA",
    "Сакраменто":"SAC",
    "Мемфис":"MEM",
    "Майами":"MIA",
    "Филадельфия": "PHI",
    "Милуоки":"MIL",
    "Вашингтон":"WAS",
    "Орландо":"ORL",
    "Денвер":"DEN",
    "Атланта":"ATL",
    "Нью-Йорк": "NYK",
    "Миннесота":"MIN",
    "Бруклин": "BKN"
}

def get_broadcasts_today():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url,wait_until="networkidle",timeout=0)

        video_links = []
        # Extract all video links
        for el in page.query_selector_all("a"):
            link = el.get_attribute('href')
            name = el.get_attribute('title')
            if link is not None and link.__contains__("/playlist/") and name is not None:
                link = f"https://vkvideo.ru/{link}"
                video = {'link':link, 'name':name}
                video_links.append(video)
        browser.close()
        return video_links

def map_broadcast_links(video_links: list[str]):
    formatted_video_links = []
    today = datetime.now() - timedelta(days=1)
    tomorrow = datetime.now() + timedelta(days=1)
    for i in video_links:
        splitted_name = i['name'].split(" | ")
        match_name = splitted_name[0]
        str_date = splitted_name[2]
        date = datetime.strptime(str_date, "%d.%m.%y")
        if date >= today and date <= tomorrow:
            match_name_splitted = match_name.split(" — ")
            home_team_ru = match_name_splitted[0]
            away_team_ru = match_name_splitted[1]
            home_team = dictionary[home_team_ru]
            away_team = dictionary[away_team_ru]
            link = i['link']
            video = {
                'matchup':home_team+'-'+away_team,
                'home_team':home_team,
                'away_team':away_team,
                'date':str_date,
                'link':link
            }
            formatted_video_links.append(video)
    return formatted_video_links


def save_broadcast_links(video_links):
    fomatted_video_links = map_broadcast_links(video_links)
    with open("video_links.json", "w", encoding="utf-8") as f:
        json.dump(fomatted_video_links, f, ensure_ascii=False, indent=4)

def scrape_and_save_links():
    links = get_broadcasts_today()
    save_broadcast_links(links)    

def print_hello():
    print('hello')

def run():
    scheduler = BackgroundScheduler()
    cet = timezone("Europe/Paris")  # Central European Time
    trigger = CronTrigger(hour=15, minute=0, timezone=cet)
    scheduler.add_job(print_hello, trigger)

    print("Scheduler started. Waiting for next run...")
    scheduler.start()

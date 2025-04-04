import requests
import json
from datetime import datetime
import pytz
import os

def convert_time(utc_datetime_str: str, time_zone: str) -> str:
    # The provided UTC datetime string
    utc_datetime_str
    # Parse the UTC datetime string to a datetime object
    utc_time = datetime.strptime(utc_datetime_str, "%Y-%m-%dT%H:%M:%SZ")
    # Add the UTC timezone information to the datetime object
    utc_time = pytz.utc.localize(utc_time)
    # Convert UTC to your local time (for example, Eastern Time)
    local_timezone = pytz.timezone(time_zone)  # Change to your local timezone
    local_time = utc_time.astimezone(local_timezone)
    return str(local_time)

def get_logo(tricode:str):
    path:str = os.getcwd() + "/logos.json"
    with open(path, 'r') as j:
        data = json.load(j)
        logo_url = data[tricode]
        return logo_url

def get_todays_games(time_zone:str) -> str:
    s = requests.get('https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json')
    json_data = s.json()
    games = json_data['leagueSchedule']['gameDates']

    now = datetime.now()
    formatted_now = now.strftime("%m/%d/%Y")
    formatted_now = formatted_now + ' 00:00:00'
    games_today = [x for x in games if x['gameDate'] == formatted_now]
    output: list = []
    for i in range(len(games_today[0]['games'])):
        home_team:str = str(games_today[0]['games'][i]['homeTeam']['teamCity']) + ' ' + str(games_today[0]['games'][i]['homeTeam']['teamName'])
        away_team = str(games_today[0]['games'][i]['awayTeam']['teamCity']) + ' ' + str(games_today[0]['games'][i]['awayTeam']['teamName'])
        time = convert_time(games_today[0]['games'][i]['gameDateTimeUTC'], time_zone)
        venue = games_today[0]['games'][i]['arenaName']
        home_team_logo = games_today[0]['games'][i]['homeTeam']['teamTricode']
        away_team_logo = games_today[0]['games'][i]['awayTeam']['teamTricode']
        game = {
            'home_team':home_team,
            'home_team_logo': home_team_logo,
            'away_team':away_team,
            'away_team_logo': away_team_logo,
            'time':time,
            'venue':venue
        }
        output.append(game)
    return output
import requests
import json
from datetime import datetime
import pytz

def convert_time(utc_datetime_str: str) -> str:
    # The provided UTC datetime string
    utc_datetime_str
    # Parse the UTC datetime string to a datetime object
    utc_time = datetime.strptime(utc_datetime_str, "%Y-%m-%dT%H:%M:%SZ")
    # Add the UTC timezone information to the datetime object
    utc_time = pytz.utc.localize(utc_time)
    # Print the UTC time
    #print("UTC time:", utc_time)
    # Convert UTC to your local time (for example, Eastern Time)
    local_timezone = pytz.timezone('Europe/Paris')  # Change to your local timezone
    local_time = utc_time.astimezone(local_timezone)
    # Print the local time
    print("Local time:", local_time)
    return str(local_time)

def get_todays_games() -> str:
    s = requests.get('https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json')
    json_data = s.json()
    games = json_data['leagueSchedule']['gameDates']

    now = datetime.now()
    formatted_now = now.strftime("%m/%d/%Y")
    formatted_now = formatted_now + ' 00:00:00'
    games_today = [x for x in games if x['gameDate'] == formatted_now]
    output:str = ''
    for i in range(len(games_today[0]['games'])):
        home_team:str = str(games_today[0]['games'][i]['homeTeam']['teamCity']) + ' ' + str(games_today[0]['games'][i]['homeTeam']['teamName'])
        vs:str = ' vs '
        away_team = str(games_today[0]['games'][i]['awayTeam']['teamCity']) + ' ' + str(games_today[0]['games'][i]['awayTeam']['teamName'])
        time = convert_time(games_today[0]['games'][i]['gameDateTimeUTC'])
        output += home_team + vs + away_team + '\n' + time + '\n\n'
    return output
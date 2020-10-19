import api_client
import json
from flask import Markup
from flask_table import Table, Col
import dateutil.parser
from datetime import datetime
'''
{
    "status": "Match Finished", 
    "league": 
        {   
            "country": "England", 
            "flag": "https://media.api-sports.io/flags/gb.svg", 
            "name": "Premier League", 
            "logo": "https://media.api-sports.io/football/leagues/39.png"
        }, 
    "referee": "C. Kavanagh", 
    "homeTeam": 
        {
            "logo": "https://media.api-sports.io/football/teams/36.png", 
            "team_id": 36, 
            "team_name": "Fulham"
        }, 
    "league_id": 2790, 
    "secondHalfStart": 1599913800, 
    "statusShort": "FT", 
    "venue": "Craven Cottage", 
    "event_timestamp": 1599910200, 
    "round": "Regular Season - 1", 
    "awayTeam": 
        {
            "logo": "https://media.api-sports.io/football/teams/42.png", 
            "team_id": 42, 
            "team_name": "Arsenal"
        }, 
    "score": 
        {
            "halftime": "0-1", 
            "extratime": null, 
            "fulltime": "0-3", 
            "penalty": null
        }, 
    "fixture_id": 592143, 
    "event_date": "2020-09-12T11:30:00+00:00", 
    "elapsed": 90, 
    "firstHalfStart": 1599910200, 
    "goalsAwayTeam": 3, 
    "goalsHomeTeam": 0
}
'''


class Fixtures(Table):
    def sort_url(self, col_id, reverse=False):
        pass
    timestamp = Col('')
    home_team_logo = Col('')
    home_team_name = Col('')
    score = Col('')
    away_team_logo = Col('')
    away_team_name = Col('')
    status_short = Col('')


class Fixture(object):
    def __init__(self, timestamp, home_team_logo, home_team_name, score, away_team_logo, away_team_name, status_short, matchday):
        def __getitem__(self, item):
            return self.Fixture[item]
        # self.home_team_id = home_team_id
        self.timestamp = timestamp
        self.home_team_name = home_team_name
        self.home_team_logo = home_team_logo
        # self.away_team_id = away_team_id
        self.away_team_name = away_team_name
        self.away_team_logo = away_team_logo
        self.score = score
        self.status_short = status_short
        self.matchday = matchday


def datetime_to_readable(iso_datetime):
    # "event_date": "2020-09-12T14:00:00+00:00"
    return datetime.strftime(dateutil.parser.isoparse(iso_datetime), '%d %b %H:%M')


def get_fixture_data(input):

    #TODO: this is stupid, redo. Find a way to distinct how data should be retrieved (API vs DB vs else)

    if type(input) == int:
        data = api_client.get_fixtures_by_league_id(input)
    else:
        f = open(input)
        data = json.load(f)
    fixtures_data = data['api']['fixtures']

    return fixtures_data


def populate_table_data(i):
    table_data = get_fixture_data(i)

    items = []
    for row in table_data:
        timestamp = row['event_date']
        home_team = row['homeTeam']
        away_team = row['awayTeam']
        # home_team_id = home_team['team_id']
        home_team_name = home_team['team_name']
        home_team_logo = home_team['logo']
        # away_team_id = away_team['team_id']
        away_team_name = away_team['team_name']
        away_team_logo = away_team['logo']
        score = row['score']['fulltime']
        status_short = row['statusShort']
        matchday = row['round']

        items.append(Fixture(datetime_to_readable(timestamp), Markup('<img src =' + home_team_logo + ' style="width:20px;height:20px;">'), home_team_name, score, Markup('<img src =' + away_team_logo + ' style="width:20px;height:20px;">'), away_team_name, status_short, matchday))
    return items


def build_table(i):

    items = populate_table_data(i)
    table = Fixtures(items)

    return table.__html__()
import json

import dateutil

import api_client
from flask_table import Table, Col
from flask import Markup

from datetime import datetime

from kickoff_time import KickOffTime


class FixtureBriefInfo(object):
    def __init__(self, timestamp, home_team_logo, home_team_name, score, away_team_logo, away_team_name, status_short,
                 matchday, id, country_flag, league_name, league_id):
        self.id = id
        self.timestamp = timestamp
        self.home_team_name = home_team_name
        self.home_team_logo = home_team_logo
        self.away_team_name = away_team_name
        self.away_team_logo = away_team_logo
        self.score = score
        self.status_short = status_short
        self.matchday = matchday
        self.country_flag = country_flag
        self.league_id = league_id
        self.league_name = league_name


def build_fixture_stats(fixture_id):
    # fixture = [] # TODO: this is stupid, don't use list here, research!
    fixture_info = api_client.get_fixture_by_id(fixture_id)
    fixture_stats = fixture_info['api']['fixtures'][0]
    fixture_id = fixture_stats['fixture_id']
    timestamp = fixture_stats['event_date']
    home_team = fixture_stats['homeTeam']
    away_team = fixture_stats['awayTeam']
    home_team_name = home_team['team_name']
    home_team_logo = home_team['logo']
    away_team_name = away_team['team_name']
    away_team_logo = away_team['logo']
    score = fixture_stats['score']['fulltime'] if fixture_stats['score']['fulltime'] is not None else datetime_to_readable(timestamp).time
    status_short = fixture_stats['statusShort']
    matchday = fixture_stats['round']
    country_flag = fixture_stats['league']['flag']
    league_id = fixture_stats['league_id']
    league_name = fixture_stats['league']['name']

    # return FixtureBriefInfo(datetime_to_readable(timestamp).date, Markup(
    #         '<img src =' + home_team_logo + ' style="width:70px;height:70px;">'), home_team_name, Markup('<a href = "/fixture/'+ str(fixture_id) + '">' + str(score) +'</a>'), Markup(
    #         '<img src =' + away_team_logo + ' style="width:70px;height:70px;">'), away_team_name, status_short,
    #                                                matchday, fixture_id, Markup(
    #             '<img src =' + country_flag + ' style="width:20px;height:20px;">'), Markup('<a href = "/league/' + str(league_id) + '">' + league_name + '</a>'), league_id)

    return FixtureBriefInfo(datetime_to_readable(timestamp).date, home_team_logo, home_team_name, str(score),
                            away_team_logo, away_team_name, status_short, matchday, fixture_id, country_flag, league_name,
                            league_id)

    # return fixture


def datetime_to_readable(iso_datetime):
    # "event_date": "2020-09-12T14:00:00+00:00"
    datetime_hr = datetime.strftime(dateutil.parser.isoparse(iso_datetime), '%d %b %H:%M')
    date_hr = f'{datetime_hr.split(" ")[0]} {datetime_hr.split(" ")[1]}'
    time_hr = f'{datetime_hr.split(" ")[2]}'
    return KickOffTime(date_hr, time_hr)


class FixtureEvents(object):
    def __init__(self, events):
        self.events = events


'''
{
        "elapsed": 35,
        "elapsed_plus": null,
        "team_id": 532,
        "teamName": "Valencia",
        "player_id": 930,
        "player": "C. Soler",
        "assist_id": null,
        "assist": null,
        "type": "Goal",
        "detail": "Penalty",
        "comments": null
      },
'''


class EventsTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass

    elapsed = Col('')
    type = Col('')
    player = Col('')
    teamName = Col('')


class Event(object):
    def __init__(self, elapsed, elapsed_plus, team_id, teamName, player_id, player, assist_id, assist, type, detail,
                 comments):
        self.elapsed = elapsed
        self.elapsed_plus = elapsed_plus
        self.team_id = team_id
        self.teamName = teamName
        self.player_id = player_id
        self.player = player
        self.assist_id = assist_id
        self.assist = assist
        self.type = type
        self.detail = detail
        self.comments = comments


def get_fixture_events(fixture_id):
    # TODO: this is stupid, redo. Find a way to distinct how data should be retrieved (API vs DB vs else)

    if type(fixture_id) == int:
        data = api_client.get_fixture_events_by_fixture_id(fixture_id)
    else:
        f = open(fixture_id)
        data = json.load(f)
    fixture_events_data = data['api']['events']

    return fixture_events_data


def get_fixture_by_id(fixture_id):
    if type(fixture_id) == int:
        data = api_client.get_fixture_by_id(fixture_id)
    else:
        f = open(fixture_id)
        data = json.load(f)
    fixture_data = data['api']['fixtures']

    return fixture_data


def populate_table_data(i):
    table_data = get_fixture_events(i)

    items = []
    for row in table_data:
        elapsed = row['elapsed']
        elapsed_plus = row['elapsed_plus']
        team_id = row['team_id']
        team_name = row['teamName']
        player_id = row['player_id']
        player = row['player']
        assist_id = row['assist_id']
        assist = row['assist']
        type = row['type']
        detail = row['detail']
        comments = row['comments']

        items.append(Event(elapsed, elapsed_plus, team_id, team_name, player_id, player, assist_id, assist, type, detail,
                           comments))
    return items

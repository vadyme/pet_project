import json

import api_client
from flask_table import Table, Col


class FixtureBriefInfo(object):
    def __init__(self, timestamp, home_team_logo, home_team_name, score, away_team_logo, away_team_name, status_short,
                 matchday, id, country_flag, league_name, league_id):
        def __getitem__(self, item):
            return self.FixtureBriefInfo[item]

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

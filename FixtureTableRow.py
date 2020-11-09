import api_client
import json
from flask import Markup
from flask_table import Table, Col
import dateutil.parser
from datetime import datetime

# TODO: add Events


class FixturesTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass
    timestamp = Col('')
    home_team_logo = Col('')
    home_team_name = Col('')
    score = Col('')
    away_team_logo = Col('')
    away_team_name = Col('')
    status_short = Col('')


class FixtureTableRow(object):
    def __init__(self, timestamp, home_team_logo, home_team_name, score, away_team_logo, away_team_name, status_short, matchday, id):
        def __getitem__(self, item):
            return self.FixtureTableRow[item]
        self.id = id
        self.timestamp = timestamp
        self.home_team_name = home_team_name
        self.home_team_logo = home_team_logo
        self.away_team_name = away_team_name
        self.away_team_logo = away_team_logo
        self.score = score
        self.status_short = status_short
        self.matchday = matchday


def datetime_to_readable(iso_datetime):
    # "event_date": "2020-09-12T14:00:00+00:00"
    return datetime.strftime(dateutil.parser.isoparse(iso_datetime), '%d %b %H:%M')


def get_fixtures_by_league_id(input):

    #TODO: this is stupid, redo. Find a way to distinct how data should be retrieved (API vs DB vs else)

    if type(input) == int:
        data = api_client.get_fixtures_by_league_id(input)
    else:
        f = open(input)
        data = json.load(f)
    fixtures_data = data['api']['fixtures']

    return fixtures_data


def build_fixtures_table(i):

    # TODO: there is really no need to call this API often. Since the schedule is pre-defined for the entire season,
    # just save it somewhere and read, periodically updating if there are any changes to schedule.

    table_data = get_fixtures_by_league_id(i)

    fixture_table_rows = []
    for row in table_data:
        fixture_id = row['fixture_id']
        timestamp = row['event_date']
        home_team = row['homeTeam']
        away_team = row['awayTeam']
        home_team_name = home_team['team_name']
        home_team_logo = home_team['logo']
        away_team_name = away_team['team_name']
        away_team_logo = away_team['logo']
        score = row['score']['fulltime']
        status_short = row['statusShort']
        matchday = row['round']

        fixture_table_rows.append(FixtureTableRow(datetime_to_readable(timestamp), Markup('<img src =' + home_team_logo + ' style="width:20px;height:20px;">'), home_team_name, score, Markup('<img src =' + away_team_logo + ' style="width:20px;height:20px;">'), away_team_name, status_short, matchday, fixture_id))
    return fixture_table_rows


def is_live_fixture(fixture):

    is_live = True if (fixture.status_short not in ['FT', 'NS']) else False
    return is_live


def live_fixture_data(fixture):

    # TODO: save a response as an JSON file and use it instead of pulling the API

    f = api_client.get_fixture_by_id(fixture.id)
    live_fixture_stats = f['api']['fixtures'][0]
    fixture.status_short = live_fixture_stats['elapsed']
    # "fulltime": "0-3"
    live_score = '{}-{}'.format(str(live_fixture_stats['goalsHomeTeam']), str(live_fixture_stats['goalsAwayTeam']))
    fixture.score = live_score

    return FixtureTableRow
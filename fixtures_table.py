import api_client
import json
from flask import Markup
from flask_table import Table, Col
import dateutil.parser
from datetime import datetime
from fixture import FixtureBriefInfo
from kickoff_time import KickOffTime


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
    # league_name = Col('')


class MultipleLeaguesFixturesTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass

    timestamp = Col('')
    home_team_logo = Col('')
    home_team_name = Col('')
    score = Col('')
    away_team_logo = Col('')
    away_team_name = Col('')
    status_short = Col('')
    country_flag = Col('')
    league_name = Col('')


def datetime_to_readable(iso_datetime):
    # "event_date": "2020-09-12T14:00:00+00:00"
    datetime_hr = datetime.strftime(dateutil.parser.isoparse(iso_datetime), '%d %b %H:%M')
    date_hr = f'{datetime_hr.split(" ")[0]} {datetime_hr.split(" ")[1]}'
    time_hr = f'{datetime_hr.split(" ")[2]}'
    return KickOffTime(date_hr, time_hr)


def get_fixtures_by_league_id(input):
    # TODO: this is stupid, redo. Find a way to distinct how data should be retrieved (API vs DB vs else)

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
        score = row['score']['fulltime'] if row['score']['fulltime'] is not None else datetime_to_readable(timestamp).time
        status_short = row['statusShort']
        matchday = row['round']
        country_flag = row['league']['flag']
        league_id = row['league_id']
        league_name = row['league']['name']

        fixture_table_rows.append(FixtureBriefInfo(datetime_to_readable(timestamp).date, Markup(
            '<img src =' + home_team_logo + ' style="width:20px;height:20px;">'), home_team_name, Markup('<a href = "/fixture/'+ str(fixture_id) + '">' + str(score) +'</a>'), Markup(
            '<img src =' + away_team_logo + ' style="width:20px;height:20px;">'), away_team_name, status_short,
                                                   matchday, fixture_id, Markup(
                '<img src =' + country_flag + ' style="width:20px;height:20px;">'), Markup('<a href = "/league/' + str(league_id) + '">' + league_name + '</a>'), league_id))
    return fixture_table_rows


def is_live_fixture(fixture):
    is_live = True if (fixture.status_short not in ['FT', 'NS']) else False
    return is_live


def live_fixture_data(fixture):
    # TODO: save a response as an JSON file and use it instead of pulling the API
    # TODO: bug - a live fixture is being displayed twice

    f = api_client.get_fixture_by_id(fixture.id)
    live_fixture_stats = f['api']['fixtures'][0]
    fixture.status_short = live_fixture_stats['elapsed']
    # "fulltime": "0-3"
    live_score = '{}-{}'.format(str(live_fixture_stats['goalsHomeTeam']), str(live_fixture_stats['goalsAwayTeam']))
    fixture.score = live_score

    return fixture

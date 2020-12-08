import json
import dateutil
from dateutil import parser
import api_client
from flask_table import Table, Col
from datetime import datetime
from kickoff_time import KickOffTime
from league import urlify_league_name
import dao


class Fixture(object):
    def __init__(self, kickoff_date, home_team_logo, home_team_name, score, away_team_logo, away_team_name, status_short,
                 matchday, id, country_flag, league_name, league_id, urlified_league_name, timestamp):
        self.id = id
        self.kickoff_date = kickoff_date
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
        self.urlified_league_name = urlified_league_name
        self.timestamp = timestamp


# TODO: find the similar code and reuse
def create_fixture_object(fixture_id):

    # gets details from API
    # fixture_info = api_client.get_fixture_by_id(fixture_id)
    # fixture_stats = fixture_info['api']['fixtures'][0]

    # gets details from the DB
    # TODO: use this not only for DB fixtures, but for API fixtures as well
    fixture_info = dao.get_fixture_details(fixture_id)

    fixture_stats = fixture_info[0]

    kickoff_date = fixture_stats['event_date']
    timestamp = fixture_stats['event_timestamp']
    home_team = fixture_stats['homeTeam']
    away_team = fixture_stats['awayTeam']
    home_team_name = home_team['team_name']
    home_team_logo = home_team['logo']
    away_team_name = away_team['team_name']
    away_team_logo = away_team['logo']
    score = fixture_stats['score']['fulltime'] if fixture_stats['score']['fulltime'] is not None else datetime_to_readable(kickoff_date).time
    status_short = fixture_stats['statusShort']
    matchday = fixture_stats['round']
    country_flag = fixture_stats['league']['flag'] if fixture_stats['league']['flag'] is not None else fixture_stats['league']['logo']
    league_id = fixture_stats['league_id']
    league_name = fixture_stats['league']['name']
    urlified_league_name = urlify_league_name(league_name)

    return Fixture(
        datetime_to_readable(kickoff_date),
        home_team_logo,
        home_team_name,
        str(score),
        away_team_logo,
        away_team_name,
        status_short,
        matchday,
        fixture_id,
        country_flag,
        league_name,
        league_id,
        urlified_league_name,
        timestamp
    )


def datetime_to_readable(iso_datetime):
    # "event_date": "2020-09-12T14:00:00+00:00"
    datetime_hr = datetime.strftime(parser.isoparse(iso_datetime), '%d %b %H:%M')
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

        items.append(Event(elapsed,
                           elapsed_plus,
                           team_id,
                           team_name,
                           player_id,
                           player,
                           assist_id,
                           assist,
                           type,
                           detail,
                           comments))
    return items


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
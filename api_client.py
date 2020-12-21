import requests

API_KEY = ''
BASE_URL_V2 = 'https://api-football-v1.p.rapidapi.com/v2'
BASE_URL_V3 = 'https://v3.football.api-sports.io'
FIXTURES_URL_V2 = f'{BASE_URL_V2}/{"fixtures"}'
FIXTURES_URL_V3 = f'{BASE_URL_V3}/{"fixtures"}'
EVENTS_URL_V2 = f'{BASE_URL_V2}/{"events"}'
EVENTS_URL_V3 = f'{FIXTURES_URL_V3}/{"events"}'
FIXTURES_LEAGUE_URL = f'{FIXTURES_URL_V2}/{"league"}'
HEADER = {'X-RapidAPI-Key': API_KEY}

HOST = 'v3.football.api-sports.io'


def s():
    s = requests.Session()
    s.headers.update(HEADER)

    return s


def do_request(url):
    sess = s()
    resp = sess.get(url)

    return resp.json()


def get_fixtures_by_league_id(league_id):
    url = f'{FIXTURES_LEAGUE_URL}/{league_id}'
    return do_request(url)


def get_fixtures_by_league_and_round(league_id, round_id):
    url = f'{FIXTURES_LEAGUE_URL}/{league_id}/{round_id}'
    return do_request(url)


def get_fixtures_by_league_and_date(league_id, date):
    url = f'{FIXTURES_LEAGUE_URL}/{league_id}/{date}'
    return do_request(url)


def get_current_round_by_league_id(league_id):
    url = f'{FIXTURES_URL_V2}/{"rounds"}/{league_id}/{"current"}'
    return do_request(url)


def get_rounds_by_league(league_id):
    # https://api-football-v1.p.rapidapi.com/v2/fixtures/rounds/{league_id}
    url = f'{FIXTURES_URL_V2}/rounds/{league_id}'
    return do_request(url)

def get_standings_by_league_id(league_id):
    url = f'{BASE_URL_V2}/{"leagueTable"}/{league_id}'
    return do_request(url)


def get_available_leagues():
    url = f'{BASE_URL_V2}/{"leagues"}'
    return do_request(url)


def get_top_scores_by_league_id(league_id):
    url = f'{BASE_URL_V2}/{"topscorers"}/{league_id}'
    return do_request(url)


def get_fixture_by_id(fixture_id):
    url = f'{FIXTURES_URL_V2}/{"id"}/{fixture_id}'
    return do_request(url)


def get_fixture_events_by_fixture_id(fixture_id):
    url = f'{EVENTS_URL_V2}/{fixture_id}'
    return do_request(url)

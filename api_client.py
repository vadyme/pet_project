import requests

key = ''
base_url_v2 = 'https://api-football-v1.p.rapidapi.com/v2'
base_url_v3 = 'https://v3.football.api-sports.io'
fixtures_url_v2 = '{}/{}'.format(base_url_v2, 'fixtures')
fixtures_url_v3 = '{}/{}'.format(base_url_v3, 'fixtures')
events_url_v2 = '{}/{}'.format(base_url_v2, 'events')
events_url_v3 = '{}/{}'.format(fixtures_url_v3, 'events')
fixtures_league_url = '{}/{}'.format(fixtures_url_v2, 'league')
header = {'X-RapidAPI-Key': key}

host = 'v3.football.api-sports.io'


def s():
    s = requests.Session()
    s.headers.update(header)

    return s


def get_fixtures_by_league_id(league_id):

    sess = s()
    url = '{}/{}'.format(fixtures_league_url, league_id)
    resp = sess.get(url)

    return resp.json()


def get_fixtures_by_league_and_round(league_id, round_id):

    sess = s()
    url = '{}/{}/{}'.format(fixtures_league_url, league_id, round_id)
    resp = sess.get(url)

    return resp.json()


def get_fixtures_by_league_and_date(league_id, date):

    sess = s()
    url = '{}/{}/{}'.format(fixtures_league_url, league_id, date)
    resp = sess.get(url)

    return resp.json()


def get_current_round_by_league_id(league_id):
    sess = s()
    url = '{}/{}/{}/{}'.format(fixtures_url_v2, 'rounds', league_id, 'current')
    resp = sess.get(url)

    return resp.json()


def get_standings_by_league_id(league_id):
    sess = s()
    url = '{}/{}/{}'.format(base_url_v2, 'leagueTable', league_id)
    resp = sess.get(url)

    return resp.json()


def get_available_leagues():
    sess = s()
    url = '{}/{}'.format(base_url_v2, 'leagues')
    resp = sess.get(url)

    return resp.json()


def get_top_scores_by_league_id(league_id):
    # "https://api-football-v1.p.rapidapi.com/v2/topscorers/{league_id}"
    sess = s()
    url = '{}/{}/{}'.format(base_url_v2, 'topscorers', league_id)
    resp = sess.get(url)

    return resp.json()


def get_fixture_by_id(fixture_id):
    # get("https://api-football-v1.p.rapidapi.com/v2/fixtures/id/{fixture_id}");
    sess = s()
    url = '{}/{}/{}'.format(fixtures_url_v2, 'id', fixture_id)
    resp = sess.get(url)

    return resp.json()


def get_fixture_events_by_fixture_id(fixture_id):
    # get("https://api-football-v1.p.rapidapi.com/v2/events/{fixture_id}");
    sess = s()
    url = '{}/{}'.format(events_url_v2, fixture_id)
    resp = sess.get(url)

    return resp.json()
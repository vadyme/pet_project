import requests

key = ''
base_url = 'https://api-football-v1.p.rapidapi.com/v2'
fixtures_url = '{}/{}'.format(base_url, 'fixtures')
fixtures_league_url = '{}/{}'.format(fixtures_url, 'league')
header = {'X-RapidAPI-Key': key}


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
    url = fixtures_url + 'rounds/' + str(league_id) + '/current'
    resp = sess.get(url)

    return resp.json()


def get_standings_by_league_id(league_id):
    sess = s()
    url = base_url + '/leagueTable/' + str(league_id)
    resp = sess.get(url)

    return resp.json()


def get_available_leagues():
    sess = s()
    url = base_url + '/leagues'
    resp = sess.get(url)

    return resp.json()
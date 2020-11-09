import unittest
import json
from Fixture import Fixture, live_fixture_data

fixture_json = './models/response_get_fixture_by_id.json'
live_fixture_json = './models/response_get_live_fixture_by_id.json'


def create_fixture(json_file):
    f = open(fixture_json)
    data = json.load(f)
    fixture_data = data['api']['fixtures'][0]
    f.close()

    fixture_id = fixture_data['fixture_id']
    timestamp = fixture_data['event_date']
    home_team = fixture_data['homeTeam']
    away_team = fixture_data['awayTeam']
    # home_team_id = home_team['team_id']
    home_team_name = home_team['team_name']
    home_team_logo = home_team['logo']
    # away_team_id = away_team['team_id']
    away_team_name = away_team['team_name']
    away_team_logo = away_team['logo']
    score = fixture_data['score']['fulltime']
    status_short = fixture_data['statusShort']
    matchday = fixture_data['round']

    fixture = Fixture(timestamp, home_team_logo, home_team_name, score, away_team_logo, away_team_name,
                           status_short, matchday, id)
    return fixture


class TestFixture(unittest.TestCase):

    def setUp(self):
        self.fixture = create_fixture(fixture_json)
        # self.live_fixture = create_fixture(live_fixture_json)

        f = open(live_fixture_json)
        self.data = json.load(f)
        f.close()

    def test_live_fixture_data(self):

        live_fixture_stats = self.data['api']['fixtures'][0]
        live_score = '{}-{}'.format(str(live_fixture_stats['goalsHomeTeam']), str(live_fixture_stats['goalsAwayTeam']))

        self.fixture.status_short = live_fixture_stats['elapsed']
        self.fixture.score = live_score

        self.assertEqual(self.fixture.status_short, 40)
        self.assertEqual(self.fixture.score, '1-1')

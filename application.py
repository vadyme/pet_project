from flask import Flask, render_template

import Topscorers
import fixture
import standing_table
import fixtures_table, matchday
from fixtures_table import FixturesTable
from standing_table import StandingTable
from Topscorers import TopscorersTable
from fixture import EventsTable

app = Flask(__name__)

# json_file = './models/standing_table.json'
# fixtures_json = './models/response_get_fixtures_by_league_id.json'

# league_id = 2833


@app.route('/', methods=['GET'])
def index():

    current_matchday_fixtures = fixtures_table.MultipleLeaguesFixturesTable(matchday.get_current_matchday_for_multiple_leagues())

    return render_template('index.html', current_matchday_fixtures=current_matchday_fixtures)


@app.route('/test/<int:league_id>')
def test_page(league_id):
    matchday_id = matchday.get_current_matchday_id(league_id)
    matchday_fixtures = FixturesTable(matchday.get_current_matchday_fixtures(league_id))
    table = StandingTable(standing_table.build_standings_table(league_id))
    topscorers = TopscorersTable(Topscorers.populate_table_data(league_id))

    return render_template('matchday_template.html', methods=['GET'],
                           matchday_id=matchday_id, fixtures=matchday_fixtures, table=table, topscorers=topscorers)


@app.route('/dev/fixture/<int:fixture_id>')
def fixture_events_page(fixture_id):
    fixture_events = EventsTable(fixture.populate_table_data(fixture_id))

    return render_template('fixture_events.html', methods=['GET'], fixture_events=fixture_events)


if __name__ == "__main__":
    app.run(debug=True)

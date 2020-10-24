from flask import Flask, render_template, request
import standing_table
import fixture, matchday
from fixture import Fixtures
from standing_table import StandingTable

app = Flask(__name__)

# json_file = './models/standing_table.json'
# fixtures_json = './models/fixtures_by_league.json'

# league_id = 2833


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
    # return standing_table.build_table(league_id)


@app.route('/standings-table/<int:league_id>', methods=['GET'])
def standings_table(league_id):
    return standing_table.build_table(league_id)


@app.route('/fixtures/<int:league_id>')
def fixtures(league_id):
    return fixture.build_table(league_id)


@app.route('/current/<int:league_id>')
def current(league_id):
    return matchday.build_table(league_id)


@app.route('/test/<int:league_id>')
def test_page(league_id):

    matchday_fixtures = Fixtures(matchday.get_current_matchday_fixtures(league_id))
    table = StandingTable(standing_table.populate_table_data(league_id))

    return render_template('matchday_template.html', methods=['GET'], fixtures=matchday_fixtures, table=table)


if __name__ == "__main__":
    app.run(debug=True)

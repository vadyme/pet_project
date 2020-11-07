from flask import Flask, render_template, request
import standing_table
import Fixture, Matchday
from Fixture import Fixtures
from standing_table import StandingTable
from Topscorers import Topscorer, TopscorersTable, populate_table_data

app = Flask(__name__)

# json_file = './models/standing_table.json'
# fixtures_json = './models/fixtures_by_league.json'

# league_id = 2833


@app.route('/', methods=['GET'])
def index():

    current_matchday_fixtures = Fixtures(Matchday.get_current_matchday_for_multiple_leagues())

    return render_template('index.html', current_matchday_fixtures=current_matchday_fixtures)


@app.route('/test/<int:league_id>')
def test_page(league_id):
    matchday_id = Matchday.get_current_matchday_id(league_id)
    matchday_fixtures = Fixtures(Matchday.get_current_matchday_fixtures(league_id))
    table = StandingTable(standing_table.populate_table_data(league_id))
    topscorers = TopscorersTable(populate_table_data(league_id))

    return render_template('matchday_template.html', methods=['GET'], matchday_id = matchday_id, fixtures=matchday_fixtures, table=table, topscorers = topscorers)


if __name__ == "__main__":
    app.run(debug=True)

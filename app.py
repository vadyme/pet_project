from flask import Flask, render_template, request
import standing_table
import fixture, Matchday
from fixture import Fixtures
from standing_table import StandingTable
from Topscorers import Topscorer, TopscorersTable, populate_table_data

app = Flask(__name__)

# json_file = './models/standing_table.json'
# fixtures_json = './models/fixtures_by_league.json'

# league_id = 2833


@app.route('/', methods=['GET'])
def index():

    bundesliga_matchday_fixtures = Fixtures(Matchday.get_current_matchday_fixtures(2755))
    primera_matchday_fixtures = Fixtures(Matchday.get_current_matchday_fixtures(2833))
    seriea_matchday_fixtures = Fixtures(Matchday.get_current_matchday_fixtures(2857))
    epl_matchday_fixtures = Fixtures(Matchday.get_current_matchday_fixtures(2790))

    return render_template('index.html', bundesliga_matchday_fixtures=bundesliga_matchday_fixtures, primera_matchday_fixtures=primera_matchday_fixtures,
           seriea_matchday_fixtures = seriea_matchday_fixtures, epl_matchday_fixtures= epl_matchday_fixtures)
    # return standing_table.build_table(league_id)


@app.route('/standings-table/<int:league_id>', methods=['GET'])
def standings_table(league_id):
    return standing_table.build_table(league_id)


@app.route('/fixtures/<int:league_id>')
def fixtures(league_id):
    return fixture.build_table(league_id)


@app.route('/current/<int:league_id>')
def current(league_id):
    return Matchday.build_table(league_id)


@app.route('/test/<int:league_id>')
def test_page(league_id):
    matchday_id = Matchday.get_current_matchday_id(league_id).split('_')[-1]
    matchday_fixtures = Fixtures(Matchday.get_current_matchday_fixtures(league_id))
    table = StandingTable(standing_table.populate_table_data(league_id))
    topscorers = TopscorersTable(populate_table_data(league_id))

    return render_template('matchday_template.html', methods=['GET'], matchday_id=matchday_id, fixtures=matchday_fixtures, table=table, topscorers = topscorers)


@app.route('/dev/<int:league_id>')
def dev_page(league_id):

    matchday_fixtures = Fixtures(Matchday.get_current_matchday_fixtures(league_id))
    table = StandingTable(standing_table.populate_table_data(league_id))

    return render_template('matchday_template.html', methods=['GET'], fixtures=matchday_fixtures, table=table)


if __name__ == "__main__":
    app.run(debug=True)

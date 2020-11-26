from flask import Flask, render_template

import Topscorers
import fixture
import standing_table
import fixtures_table, matchday
from fixtures_table import FixturesTable
from standing_table import StandingTable
from Topscorers import TopscorersTable
from fixture import EventsTable, FixtureBriefInfo
from league import map_league_name_to_id

app = Flask(__name__)


# json_file = './models/standing_table.json'
# fixtures_json = './models/response_get_fixtures_by_league_id.json'

# league_id = 2833


@app.route('/', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    current_matchday_fixtures = fixtures_table.MultipleLeaguesFixturesTable(
        matchday.get_current_matchday_for_multiple_leagues())

    return render_template('index.html', current_matchday_fixtures=current_matchday_fixtures)


@app.route('/league/<league_name>')
def test_page(league_name):
    league_id = map_league_name_to_id(league_name)
    if league_id is not None:
        matchday_id = matchday.get_current_matchday_id(league_id)
        matchday_fixtures = FixturesTable(matchday.get_current_matchday_fixtures(league_id))
        table = StandingTable(standing_table.build_standings_table(league_id))
        topscorers = TopscorersTable(Topscorers.populate_table_data(league_id))

        return render_template('matchday_template.html', methods=['GET'],
                               matchday_id=matchday_id, fixtures=matchday_fixtures, table=table, topscorers=topscorers)
    else:
        return render_template('page_not_found.html')


@app.route('/league/<int:league_id>/matchday/<int:matchday_id>')
def matchday_page(league_id, matchday_id):
    # matchday_id = matchday.get_current_matchday_id(league_id)
    matchday_fixtures = FixturesTable(matchday.get_specific_matchday_fixtures(league_id, matchday_id))
    table = StandingTable(standing_table.build_standings_table(league_id))
    topscorers = TopscorersTable(Topscorers.populate_table_data(league_id))

    return render_template('matchday_template.html', methods=['GET'],
                           matchday_id=matchday_id, fixtures=matchday_fixtures, table=table, topscorers=topscorers)


@app.route('/fixture/<int:fixture_id>')
def fixture_events_page(fixture_id):
    fix = fixture.build_fixture_stats(fixture_id)
    timestamp = fix.timestamp
    league_name = fix.league_name
    md = fix.matchday
    home_team_logo = fix.home_team_logo
    score = fix.score
    away_team_logo = fix.away_team_logo
    elapsed = fix.status_short
    home_team_name = fix.home_team_name
    away_team_name = fix.away_team_name

    fixture_events = EventsTable(fixture.populate_table_data(fixture_id))

    return render_template('fixture_stats.html', methods=['GET'], timestamp=timestamp, league_name=league_name, md=md,
                           home_team_logo=home_team_logo, score=score, away_team_logo=away_team_logo,
                           home_team_name=home_team_name, elapsed=elapsed, away_team_name=away_team_name,
                           fixture_events=fixture_events)


if __name__ == "__main__":
    app.run(debug=True)

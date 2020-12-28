from flask import Flask, render_template, json
from werkzeug.exceptions import HTTPException
from logging.config import dictConfig

import Topscorers
import fixture
import standing_table
import matchday
from standing_table import StandingTable, Standing
from Topscorers import TopscorersTable
from league import map_league_name_to_id, get_list_of_matchdays
from week_dates_range import get_week_dates, get_day_name
from datetime import date


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    today = str(date.today())
    calendar = get_week_dates()
    matchday_fixtures = matchday.get_fixtures_by_date(today)
    day_name = f'{get_day_name(today)}, {today.split("-")[1]}/{today.split("-")[2]}'

    app.logger.info("Request to open index page")

    return render_template('index.html',
                           matchday_fixtures=matchday_fixtures,
                           calendar=calendar,
                           day_name=day_name
                           )


@app.route('/matchday/<match_date>')
def get_matchday_by_date(match_date):
    calendar = get_week_dates()
    matchday_fixtures = matchday.get_fixtures_by_date(match_date)
    day_name = f'{get_day_name(match_date)}, {match_date.split("-")[1]}/{match_date.split("-")[2]}'

    app.logger.info(f'Request to open matchday page {match_date}')

    return render_template('index.html',
                           matchday_fixtures=matchday_fixtures,
                           calendar=calendar,
                           day_name=day_name)


@app.route('/league/<league_name>')
@app.route('/league/<league_name>/<pathtomatchday>')
def test_page(league_name, pathtomatchday=None):
    league_id = map_league_name_to_id(league_name)
    # TODO: request update for fixtures in progress
    if league_id is not None:
        current_matchday = matchday.get_current_matchday_id(league_id)
        matchday_id = pathtomatchday.replace("_", " ") if pathtomatchday else current_matchday
        matchdays = reversed(get_list_of_matchdays(league_id))
        matchday_fixtures = matchday.get_fixtures_by_league_and_round(league_id, matchday_id)

        app.logger.info(f'Request to open league page {league_name}')

        return render_template('league_template.html', methods=['GET'],
                               matchdays=matchdays,
                               current_matchday=current_matchday,
                               matchday_id=matchday_id,
                               fixtures=matchday_fixtures,
                               league_name=league_name
                               )
    else:
        app.logger.error("Page not found")
        return render_template('page_not_found.html')


@app.route('/league/<league_name>/standings')
def league_standings(league_name):
    league_id = map_league_name_to_id(league_name)
    # table = StandingTable(standing_table.build_standings_table(league_id))
    table = standing_table.build_standings_table(league_id)
    current_matchday = matchday.get_current_matchday_id(league_id)
    matchdays = reversed(get_list_of_matchdays(league_id))

    return render_template('standings.html', methods=['GET'],
                           table=table,
                           league_name=league_name,
                           current_matchday=current_matchday,
                           matchdays=matchdays)



@app.route('/league/<league_name>/topscorers')
def top_scorers(league_name):
    league_id = map_league_name_to_id(league_name)
    topscorers = TopscorersTable(Topscorers.populate_table_data(league_id))
    current_matchday = matchday.get_current_matchday_id(league_id)
    matchdays = reversed(get_list_of_matchdays(league_id))

    return render_template('topscorers_template.html', methods=['GET'],
                           topscorers=topscorers,
                           league_name=league_name,
                           current_matchday=current_matchday,
                           matchdays=matchdays)


# @app.route('/league/<league_name>/matchday/<matchday_name>')
# def matchday_page(league_name, matchday_name):
#     league_id = map_league_name_to_id(league_name)
#     matchdays = get_list_of_matchdays(league_id)
#     matchday_id = matchday_name.replace("_", " ")
#     matchday_fixtures = matchday.get_fixtures_by_league_and_round(league_id, matchday_id)
#
#     return render_template('league_template.html', methods=['GET'],
#                            matchday_id=matchday_id,
#                            fixtures=matchday_fixtures,
#                            league_name=league_name,
#                            matchdays=matchdays)


@app.route('/fixture/<int:fixture_id>')
def fixture_events_page(fixture_id):
    fix = fixture.create_fixture_object(fixture_id)
    timestamp = fix.kickoff_date
    league_name = fix.league_name
    urlified_league_name = fix.urlified_league_name
    md = fix.matchday
    home_team_logo = fix.home_team_logo
    score = fix.score
    away_team_logo = fix.away_team_logo
    elapsed = fix.status_short
    home_team_name = fix.home_team_name
    away_team_name = fix.away_team_name

    # fixture_events = EventsTable(fixture.populate_table_data(fixture_id))
    fixture_events = fixture.populate_table_data(fixture_id)

    return render_template('fixture_stats.html', methods=['GET'], timestamp=timestamp, league_name=league_name, md=md,
                           home_team_logo=home_team_logo, score=score, away_team_logo=away_team_logo,
                           home_team_name=home_team_name, elapsed=elapsed, away_team_name=away_team_name,
                           fixture_events=fixture_events, urlified_league_name=urlified_league_name)


# @app.route("/update_db")
# def update():
#     league_ids = [2755, 2833, 2857, 2790]
#     for l_id in league_ids:
#         fixtures = get_fixtures_by_league_id(l_id)
#         db.db.fixtures_db_collection.insert_many(fixtures)
#     return "dbUpdated: True"


# @app.route("/test_db_connection")
# def test():
#     db.db.fixtures_db_collection.insert_one({"isLive": "True"})
#     return "It's alive!"


if __name__ == "__main__":
    app.run(debug=True)

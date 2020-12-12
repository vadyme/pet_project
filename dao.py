from db import db
import logging
from bson.json_util import dumps


def get_fixtures_by_date(date):

    logging.info("Pulling data from the DB")
    q = {"event_date": {"$regex": f'{date}.*'}}
    data = list(db.fixtures_db_collection.find(q))

    return data


def get_fixture_details(fixture_id):

    q = {"fixture_id": fixture_id}
    data = list(db.fixtures_db_collection.find(q))

    return data


def get_fixtures_by_league_and_round(league_id, round_id):
    # {"league_id": 2755, "round": "Regular Season - 10"}
    q = {"league_id": league_id, "round": round_id}
    data = list(db.fixtures_db_collection.find(q))

    return data


def update_fixture_object(fixture_id, status_short, status, elapsed, goals_home_team, goals_away_team,
                          score_ht, score_ft, score_et, score_pen ):

    data = db.fixtures_db_collection.update_one({'fixture_id': fixture_id}, {"$set": {'statusShort': status_short,
                                                                                       'status': status,
                                                                                       'elapsed': elapsed,
                                                                                       'goalsHomeTeam': goals_home_team,
                                                                                       'goalsAwayTeam': goals_away_team,
                                                                                       'score.halftime': score_ht,
                                                                                       'score.fulltime': score_ft,
                                                                                       'score.extratime': score_et,
                                                                                       'score.penalty': score_pen
                                                                              }})

    return data
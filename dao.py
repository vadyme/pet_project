from db import db
import logging
import time
from datetime import datetime
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


def update_fixture_object(event_date, event_timestamp, fixture_id, status_short, status, elapsed, goals_home_team, goals_away_team,
                          score_ht, score_ft, score_et, score_pen ):

    data = db.fixtures_db_collection.update_one({'fixture_id': fixture_id}, {"$set": {'statusShort': status_short,
                                                                                       'status': status,
                                                                                       'elapsed': elapsed,
                                                                                       'goalsHomeTeam': goals_home_team,
                                                                                       'goalsAwayTeam': goals_away_team,
                                                                                       'score.halftime': score_ht,
                                                                                       'score.fulltime': score_ft,
                                                                                       'score.extratime': score_et,
                                                                                       'score.penalty': score_pen,
                                                                                      'event_date': event_date,
                                                                                      'event_timestamp': event_timestamp
                                                                              }})

    return data


def update_multiple_fixtures(q):
    print(f' "Writing bulk @ {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))}')
    data = db.fixtures_db_collection.bulk_write(q)
    print(f' "Writing bulk complete @ {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))}')
    return data


# def get_form_by_team(team_id, league_id):
#     q = {"$and": [{"$or": [{"homeTeam.team_id": team_id}, {"awayTeam.team_id": team_id}]}, {"league_id": league_id}, {"status" :"Match Finished"}]}
#     data = list(db.fixtures_db_collection.find(q).sort('event_timestamp', -1).limit(5))
#
#     return data

# def get_form_by_team(league_id, team_id):
#     q = {"$and": [{"league_id": league_id}, {"status": "Match Finished"}, {"$or": [{"homeTeam.team_id": team_id}, {"awayTeam.team_id": team_id}]}]}
#     data = list(db.fixtures_db_collection.find(q).sort('event_timestamp', -1).limit(5))
#
#     return data

def get_form_by_team(team_id):
    q = {"$and": [{"status": "Match Finished"}, {"$or": [{"homeTeam.team_id": team_id}, {"awayTeam.team_id": team_id}]}]}
    data = list(db.fixtures_db_collection.find(q).sort('event_timestamp', -1).limit(5))

    return data


# def get_form_by_team(league_id, team_ids):
#
#     print(datetime.now())
#     team_form = []
#
#     for team_id in team_ids:
#         q = {"$and": [{"league_id": league_id}, {"status": "Match Finished"}, {"$or": [{"homeTeam.team_id": team_id}, {"awayTeam.team_id": team_id}]}]}
#         data = list(db.fixtures_db_collection.find(q).sort('event_timestamp', -1).limit(5))
#
#         team_form.append((team_id, data))
#
#     print(datetime.now())
#     return team_form
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
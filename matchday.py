# -*- coding: UTF-8 -*-

import api_client
import fixture
import dao


def get_current_matchday_id(league_id):
    current_matchday = api_client.get_current_round_by_league_id(league_id)
    # matchday_id = current_matchday['api']['fixtures'][0].split('_')[-1]
    matchday_id = current_matchday['api']['fixtures'][0]

    return matchday_id.replace("_", " ")


# TODO: is it really necessary to iterate through the entire season calendar to find current matchday fixtures?


def get_current_matchday_fixtures(league_id):
    current_matchday_id = get_current_matchday_id(league_id)
    current_matchday_fixtures = get_fixtures_by_league_and_round(league_id, current_matchday_id)

    return current_matchday_fixtures


def get_fixtures_by_league_and_date(league_id, date):
    data = api_client.get_fixtures_by_league_and_date(league_id, date)
    fixtures = data['api']['fixtures']

    return fixtures


def get_fixtures_by_league_and_round(league_id, matchday_id):
    # fixture_data = get_fixture_data(league_id)
    fixtures = dao.get_fixtures_by_league_and_round(league_id, matchday_id)
    fs = build_list_of_fixture_objects(fixtures)

    return fs


def get_fixtures_by_date(date):
    fixtures = dao.get_fixtures_by_date(date)
    fs = build_list_of_fixture_objects(fixtures)
    sorted_fixtures = sorted(fs, key=lambda x: x.timestamp.time)

    return sorted_fixtures


def build_list_of_fixture_objects(fixtures):
    # TODO: there is really no need to call this API often. Since the schedule is pre-defined for the entire season,
    # just save it somewhere and read, periodically updating if there are any changes to schedule.

    fixture_objects_list = []
    for f in fixtures:
        fixture_id = f['fixture_id']
        fixture_objects_list.append(fixture.create_fixture_object(fixture_id))

    return fixture_objects_list

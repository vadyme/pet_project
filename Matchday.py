# -*- coding: UTF-8 -*-

import api_client
from pprint import pprint
import json
from flask_table import Table, Col
from flask import Markup
from fixture import get_fixture_data, populate_table_data, Fixtures, Fixture


def get_current_matchday_id(league_id):
    current_matchday = api_client.get_current_round_by_league_id(league_id)
    matchday_id = current_matchday['api']['fixtures'][0].split('_')[-1]

    return matchday_id

def get_current_matchday_fixtures(league_id):
    current_matchday = api_client.get_current_round_by_league_id(league_id)
    # {'results': 1, 'fixtures': ['Regular_Season_-_7']}
    current_matchday_id = current_matchday['api']['fixtures'][0].split(' - ')[-1]
    current_matchday_fixtures = get_specific_matchday_fixtures(league_id, current_matchday_id)

    return current_matchday_fixtures


def get_specific_matchday_fixtures(league_id, matchday_id):
    # fixture_data = get_fixture_data(league_id)
    all_fixtures = populate_table_data(league_id)
    matchday_fixtures = []
    for Fixture in all_fixtures:
        if Fixture.matchday.split(' - ')[-1] == matchday_id.split('_')[-1]:
            matchday_fixtures.append(Fixture)

    return matchday_fixtures


def build_table(i):

    items = get_current_matchday_fixtures(i)
    table = Fixtures(items)

    return table.__html__()

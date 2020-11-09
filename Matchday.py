# -*- coding: UTF-8 -*-

import api_client
from pprint import pprint
import json
from flask_table import Table, Col
from flask import Markup
from FixtureTableRow import get_fixtures_by_league_id, build_fixtures_table, FixturesTable, FixtureTableRow, is_live_fixture, live_fixture_data
from dataclasses import dataclass


def get_current_matchday_id(league_id):
    current_matchday = api_client.get_current_round_by_league_id(league_id)
    matchday_id = current_matchday['api']['fixtures'][0].split('_')[-1]

    return matchday_id


def get_current_matchday_fixtures(league_id):
    current_matchday = api_client.get_current_round_by_league_id(league_id)
    # {'results': 1, 'fixtures': ['Regular_Season_-_7']}
    current_matchday_id = current_matchday['api']['fixtures'][0].split(' - ')[-1]
    # current_matchday_fixtures = get_specific_matchday_fixtures(league_id, current_matchday_id)
    current_matchday_fixtures = get_specific_matchday_fixtures(league_id, '9')
    return current_matchday_fixtures


def get_specific_matchday_fixtures(league_id, matchday_id):
    # fixture_data = get_fixture_data(league_id)
    all_fixtures = build_fixtures_table(league_id)
    matchday_fixtures = []
    for Fixture in all_fixtures:
        if Fixture.matchday.split(' - ')[-1] == matchday_id.split('_')[-1]:
            # TODO: if fixture is live, provide correspondent details
            if is_live_fixture(Fixture):
                live_fixture = live_fixture_data(Fixture)
                matchday_fixtures.append(live_fixture)
            matchday_fixtures.append(Fixture)

    return matchday_fixtures


# def get_specific_matchday_fixtures(league_id, matchday_id):
#     fixtures = api_client.get_fixtures_by_league_and_round(league_id, matchday_id)
#     matchday_fixtures = []
#     for Fixture in fixtures:
#         matchday_fixtures.append(Fixture)
#
#     return matchday_fixtures


def get_current_matchday_for_multiple_leagues():
    leagues = [2755, 2833, 2857, 2790]
    fixtures = []
    for id in leagues:
        fs = get_current_matchday_fixtures(id)
        for fixture in fs:
            fixtures.append(fixture)

    sorted_fixtures = sorted(fixtures, key=lambda x: x.timestamp)

    return sorted_fixtures


# def build_table(i):
#
#     items = get_current_matchday_fixtures(i)
#     table = Fixtures(items)
#
#     return table.__html__()

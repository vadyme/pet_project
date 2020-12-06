# -*- coding: UTF-8 -*-

import api_client
from fixtures_table import build_fixtures_table, is_live_fixture, live_fixture_data
import fixture
from league import urlify_league_name
import dao
from flask import Markup


def get_current_matchday_id(league_id):
    current_matchday = api_client.get_current_round_by_league_id(league_id)
    matchday_id = current_matchday['api']['fixtures'][0].split('_')[-1]

    return matchday_id


# TODO: is it really necessary to iterate through the entire season calendar to find current matchday fixtures?


def get_current_matchday_fixtures(league_id):
    current_matchday_id = get_current_matchday_id(league_id)
    current_matchday_fixtures = get_specific_matchday_fixtures(league_id, current_matchday_id)

    return current_matchday_fixtures


def get_fixtures_by_league_and_date(league_id, date):
    data = api_client.get_fixtures_by_league_and_date(league_id, date)
    fixtures = data['api']['fixtures']

    return fixtures


def get_specific_matchday_fixtures(league_id, matchday_id):
    # fixture_data = get_fixture_data(league_id)
    all_fixtures = build_fixtures_table(league_id)
    matchday_fixtures = []
    for fixture in all_fixtures:
        if fixture.matchday.split(' - ')[-1] == matchday_id.split('_')[-1]:
            if is_live_fixture(fixture):
                live_fixture = live_fixture_data(fixture)
                fixture.score = live_fixture.score
                fixture.status_short = live_fixture.status_short
            matchday_fixtures.append(fixture)

    return matchday_fixtures


# def get_current_matchday_for_multiple_leagues():
#     # TODO: this is very expensive in terms of a number of API calls. Use DB instead.
#     leagues = [2755, 2833, 2857, 2790]
#     fixtures = []
#     for league in leagues:
#         fs = get_current_matchday_fixtures(league)
#         for fixture in fs:
#             fixtures.append(fixture)
#     # TODO: sort fixtures by kick-off time
#     sorted_fixtures = sorted(fixtures, key=lambda x: x.fixture_id)
#
#     return sorted_fixtures

def get_fixtures_by_date(date):
    fixtures = dao.get_fixtures_by_date(date)
    fs = build_fixtures_by_date_table(fixtures)
    sorted_fixtures = sorted(fs, key=lambda x: x.timestamp.time)

    return sorted_fixtures

def get_matchday_by_date(date):
    leagues = [2755, 2833, 2857, 2790]
    fixtures = []
    for league in leagues:
        fs = build_fixtures_by_date_table(get_fixtures_by_league_and_date(league, date))
        for fixture in fs:
            if is_live_fixture(fixture):
                live_fixture = live_fixture_data(fixture)
                fixture.score = live_fixture.score
                fixture.status_short = live_fixture.status_short
            fixtures.append(fixture)
    sorted_fixtures = sorted(fixtures, key=lambda x: x.timestamp.time)
    return sorted_fixtures


# TODO: this is the same exact method as in fixture_table, with the exception of a single line. REFACTOR!!
def build_fixtures_by_date_table(fixtures):
    # TODO: there is really no need to call this API often. Since the schedule is pre-defined for the entire season,
    # just save it somewhere and read, periodically updating if there are any changes to schedule.

    fixture_table_rows = []
    for row in fixtures:
        fixture_id = row['fixture_id']
        timestamp = row['event_date']
        home_team = row['homeTeam']
        away_team = row['awayTeam']
        home_team_name = home_team['team_name']
        home_team_logo = home_team['logo']
        away_team_name = away_team['team_name']
        away_team_logo = away_team['logo']
        score = row['score']['fulltime'] if row['score']['fulltime'] is not None else fixture.datetime_to_readable(
            timestamp).time
        status_short = row['statusShort']
        matchday = row['round']
        country_flag = row['league']['flag'] if row['league']['flag'] is not None else row['league']['logo']
        league_id = row['league_id']
        league_name = row['league']['name']
        urlified_league_name = urlify_league_name(league_name)

        fixture_table_rows.append(fixture.FixtureBriefInfo(fixture.datetime_to_readable(timestamp),
                                                   home_team_logo,
                                                   home_team_name,
                                                   score,
                                                   away_team_logo,
                                                   away_team_name,
                                                   status_short,
                                                   matchday,
                                                   fixture_id,
                                                   country_flag,
                                                   league_name,
                                                   league_id,
                                                   urlified_league_name)
                                  )

    return fixture_table_rows

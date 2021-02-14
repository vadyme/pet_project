# -*- coding: UTF-8 -*-
import time
import aiohttp
import asyncio
import api_client
import fixture
import dao


def get_current_matchday_id(league_id):
    current_matchday = api_client.get_current_round_by_league_id(league_id)
    # matchday_id = current_matchday['api']['fixtures'][0].split('_')[-1]
    matchday_id = current_matchday['api']['fixtures'][0]

    return matchday_id.replace("_", " ")


# TODO: is it really necessary to iterate through the entire season calendar to find current matchday fixtures?


# def get_current_matchday_fixtures(league_id):
#     current_matchday_id = get_current_matchday_id(league_id)
#     current_matchday_fixtures = get_fixtures_by_league_and_round(league_id, current_matchday_id)
#
#     return current_matchday_fixtures


def get_fixtures_by_league_and_date(league_id, date):
    data = api_client.get_fixtures_by_league_and_date(league_id, date)
    fixtures = data['api']['fixtures']

    return fixtures


def get_fixtures_by_league_and_round(league_id, matchday_id):
    # fixture_data = get_fixture_data(league_id)
    fixtures = dao.get_fixtures_by_league_and_round(league_id, matchday_id)
    fs = build_list_of_fixture_objects(fixtures)
    update_if_live(fs)

    return sorted(fs, key=lambda x: (x.kickoff_date.date, x.kickoff_date.time))


def get_fixtures_by_date(date):
    fixtures = dao.get_fixtures_by_date(date)
    fs = build_list_of_fixture_objects(fixtures)

    # if kickoff time is earlier than now and the game is NS, fetch the data from API and update the DB
    # TODO: if there are multiple fixtures as above, think on sending asynchronous calls
    # update_if_live(fs)
    asyncio.run(async_update_if_live(fs))
    sorted_fixtures = sorted(fs, key=lambda x: x.kickoff_date.time)

    return sorted_fixtures


def update_if_live(fs):
    now = time.time()
    for f in fs:
        if f.timestamp < now and (f.status != 'Match Finished') or f.status_short == 'TBD':
            print(f' "The game needs an update: " {f.id} @ {time.time()}')
            fixture_update = api_client.get_fixture_by_id(f.id)
            update = fixture_update['api']['fixtures'][0]
            update_score = update['score']
            f.event_date = update['event_date']
            f.event_timestamp = update['event_timestamp']
            f.status = update['status']
            f.status_short = update['statusShort']
            f.status = update['status']
            f.elapsed = update['elapsed']
            f.goals_home_team = update['goalsHomeTeam']
            f.goals_away_team = update['goalsAwayTeam']
            f.score_ht = update_score['halftime']
            f.score_ft = update_score['fulltime']
            f.score_et = update_score['extratime']
            f.score_pen = update_score['penalty']
            # TODO: rework the fixture class, add all necessary fields; make sure to update all fields in DB
            dao.update_fixture_object(f.event_date, f.event_timestamp, f.id, f.status_short, f.status, f.elapsed, f.goals_home_team, f.goals_away_team,
                                      f.score_ht, f.score_ft, f.score_et, f.score_pen)
            print(f' "The game has been updated: " {f.id} @ {time.time()}')


async def async_update_if_live(fs):
    now = time.time()
    async with aiohttp.ClientSession() as session:
        updates = []
        for f in fs:
            if f.timestamp < now and (f.status != 'Match Finished') or f.status_short == 'TBD':
                print(f' "The game needs an update: " {f.id} @ {time.time()}')
                update = asyncio.ensure_future(update_fixture(session, f))
                updates.append(update)

        return await asyncio.gather(*updates)


async def update_fixture(session, f):
    fixture_update = api_client.get_fixture_by_id(f.id)
    update = fixture_update['api']['fixtures'][0]
    update_score = update['score']
    f.event_date = update['event_date']
    f.event_timestamp = update['event_timestamp']
    f.status = update['status']
    f.status_short = update['statusShort']
    f.status = update['status']
    f.elapsed = update['elapsed']
    f.goals_home_team = update['goalsHomeTeam']
    f.goals_away_team = update['goalsAwayTeam']
    f.score_ht = update_score['halftime']
    f.score_ft = update_score['fulltime']
    f.score_et = update_score['extratime']
    f.score_pen = update_score['penalty']
    # TODO: rework the fixture class, add all necessary fields; make sure to update all fields in DB
    dao.update_fixture_object(f.event_date, f.event_timestamp, f.id, f.status_short, f.status, f.elapsed,
                              f.goals_home_team, f.goals_away_team,
                              f.score_ht, f.score_ft, f.score_et, f.score_pen)
    print(f' "The game has been updated: " {f.id} @ {time.time()}')


def build_list_of_fixture_objects(fixtures):
    # TODO: there is really no need to call this API often. Since the schedule is pre-defined for the entire season,
    # just save it somewhere and read, periodically updating if there are any changes to schedule.

    fixture_objects_list = []
    for f in fixtures:
        fixture_id = f['fixture_id']
        fixture_objects_list.append(fixture.create_fixture_object(fixture_id))

    return fixture_objects_list

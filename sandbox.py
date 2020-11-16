import json
import api_client
from datetime import datetime
import dateutil.parser
import Matchday
from fixtures_table import FixturesTable
import time


def write_api_response_to_file(api_response, file):
    with open(file, 'w') as f:
        json.dump(api_response, f)


def write_data_to_file(data, file):
    with open(file, 'w') as f:
        f.write(data)


def read_available_leagues():
    available_leagues = []
    f = open('./models/available_leagues.json')
    data = json.load(f)
    leagues = data['api']['leagues']
    for league in leagues:
        league_name = league['name']
        league_id = league['league_id']
        country = league['country']
        season = league['season']

        if country == 'England' or country == 'Italy' or country == 'Spain':
            if season == 2020:
                print (season, country, league_id, league_name)
                available_leagues.append(str(season) + ' ' + country + ' ' + str(league_id) + ' ' + league_name)
                for league in available_leagues:
                    with open('./models/2020_top_leagues.txt', 'a') as f:
                        f.write(league)

    return available_leagues

# read_available_leagues()
# write_api_response_to_file(api_client.get, './models/matchday_fixtures.json')
# write_data_to_file(read_available_leagues(), './models/2020_leagues.txt')
# write_api_response_to_file(api_client.get_fixtures_by_league_and_round(524, 13), './models/fixtures_by_league_and_round_2020.json')
# write_api_response_to_file(api_client.get_fixtures_by_league_id(2790), 'models/response_get_fixtures_by_league_id.json')


# print datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

# def datetime_to_readable(iso_datetime):
#
#     return datetime.strftime(dateutil.parser.isoparse(iso_datetime), '%d %b %H:%M')
#
#
# # print(datetime_to_readable('2020-09-12T14:00:00+00:00'))

# 1.48 sec for current implementation

# def time_test():
#     start_time = time.time()
#     fixtures = Matchday.get_current_matchday_fixtures(2755)
#     print("--- %s seconds ---" % (time.time() - start_time))
#
#     return fixtures
#
# time_test()

# write_api_response_to_file(api_client.get_fixture_by_id(605152), './models/response_get.json')

import api_client
import json

# class Season(object):


def get_fixture_data(input):

    #TODO: this is stupid, redo. Find a way to distinct how data should be retrieved (API vs DB vs else)

    if type(input) == int:
        data = api_client.get_fixtures_by_league_id(input)
    else:
        f = open(input)
        data = json.load(f)
    fixtures_data = data['api']['fixtures']

    return fixtures_data

#
# def split_season_to_matchdays():
#     matchdays = []
#     season_fixtures = get_fixture_data(input())
#     last_round = season_fixtures[-1]['round'].split[' - '][-1]   # to undestand how many rounds does the season have
#     for i in [1, int(last_round)]:
#         # round = fixture['round']



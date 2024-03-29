import api_client
import json
from flask_table import Table, Col


class TopscorersTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass

    nationality = Col('')
    name = Col('')
    team = Col('')
    # minutes = Col('')
    goals = Col('')
    # assists = Col('')


class Topscorer(object):
    # def __init__(self, nationality, name, team, minutes, goals, assists):
    def __init__(self, nationality, name, team, goals):
        def __getitem__(self, item):
            return self.Topscorer[item]

        self.nationality = nationality
        self.name = name
        self.team = team
        # self.minutes = minutes
        self.goals = goals
        # self.assists = assists


def get_topscorers_data(input):
    # TODO: this is stupid, redo. Find a way to distinct how data should be retrieved (API vs DB vs else)

    if type(input) == int:
        data = api_client.get_top_scores_by_league_id(input)
    else:
        f = open(input)
        data = json.load(f)
    topscorers_data = data['api']['topscorers']

    return topscorers_data


def populate_table_data(i):
    table_data = get_topscorers_data(i)
    items = [Topscorer(row['goals']['total'], row['player_name'], row['team_name'], row['nationality']) for row in table_data]
    return items

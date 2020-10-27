import api_client
import json
from flask import Markup
from flask_table import Table, Col
import dateutil.parser
from datetime import datetime


class TopscorersTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass
    nationality = Col('')
    name = Col('')
    team = Col('')
    minutes = Col('')
    goals = Col('')
    assists = Col('')


class Topscorer(object):
    def __init__(self, nationality, name, team, minutes, goals, assists):
        def __getitem__(self, item):
            return self.Topscorer[item]
        self.nationality = nationality
        self.name = name
        self.team = team
        self.minutes = minutes
        self.goals = goals
        self.assists = assists


def get_topscorers_data(input):

    #TODO: this is stupid, redo. Find a way to distinct how data should be retrieved (API vs DB vs else)

    if type(input) == int:
        data = api_client.get_top_scores_by_league_id(input)
    else:
        f = open(input)
        data = json.load(f)
    topscorers_data = data['api']['topscorers']

    return topscorers_data


def populate_table_data(i):
    table_data = get_topscorers_data(i)

    items = []
    for row in table_data:
        name = row['player_name']
        team = row['team_name']
        minutes = row['games']['minutes_played']
        goals = row['goals']['total']
        nationality = row['nationality']
        assists = row['goals']['assists']

        items.append(Topscorer(goals, name, team, nationality, assists, minutes))
    return items

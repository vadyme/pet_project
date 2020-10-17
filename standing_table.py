# -*- coding: UTF-8 -*-

import api_client
import json
from flask_table import Table, Col
from flask import Markup

json_file = './models/standing_table.json'


class StandingTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass
    logo = Col('')
    rank = Col('#')
    team_name = Col('Team')
    points = Col('Pts')
    games_played = Col('P')
    wins = Col('W')
    draws = Col('D')
    losses = Col('L')
    goals_for = Col('GF')
    goals_against = Col('GA')
    form = Col('Form')


def get_table_data(input):

    #TODO: this is stupid, redo. Find a way to distinct how data should be retrieved (API vs DB vs else)

    if type(input) == int:
        data = api_client.get_standings_by_league_id(input)
    else:
        f = open(input)
        data = json.load(f)
    table_data = data['api']['standings'][0]

    return table_data


# def get_table_data_from_api_response(league_id):
#
#     data = api_client.get_standings_by_league_id(league_id)
#     table_data = data['api']['standings'][0]
#
#     return table_data


class Item(object):
    def __init__(self, logo, rank, team_name, games_played, wins, draws, losses, goals_for, goals_against, points, form):
        self.logo = logo
        self.rank = rank
        self.team_name = team_name
        self.games_played = games_played
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.points = points
        self.form = form


def populate_table_data(i):
    table_data = get_table_data(i)

    items = []
    for row in table_data:
        logo = row['logo']
        rank = row['rank']
        team_name = row['teamName']
        all_games_stats = row['all']
        games_played = all_games_stats['matchsPlayed']
        wins = all_games_stats['win']
        draws = all_games_stats['draw']
        losses = all_games_stats['lose']
        goals_for = all_games_stats['goalsFor']
        goals_against = all_games_stats['goalsAgainst']
        points = row['points']
        form = row['forme']

        items.append(Item(Markup('<img src =' + logo + ' style="width:20px;height:20px;">'), rank, team_name, games_played, wins, draws, losses, goals_for, goals_against, points, form))
    return items


def build_table(i):

    items = populate_table_data(i)
    table = StandingTable(items)

    return table.__html__()

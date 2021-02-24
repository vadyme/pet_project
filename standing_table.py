# -*- coding: UTF-8 -*-

import api_client
import json
from flask_table import Table, Col
from flask import Markup
from dao import get_form_by_team
from matchday import build_list_of_fixture_objects

json_file = './models/standing_table.json'


class Standing(object):
    def __init__(self, rank, team_id, team_name, logo, group, form, status, description, all_played,
                 all_win, all_draw, all_lose, all_goals_for, all_goals_against, goals_diff, pts):
        self.rank = rank
        self.team_id=team_id
        self.team_name = team_name
        self.team_logo = logo
        self.group = group
        self.form = form
        self.status = status
        self.description = description
        self.played = all_played
        self.win = all_win
        self.draw = all_draw
        self.lose = all_lose
        self.gf = all_goals_for
        self.ga = all_goals_against
        self.gd = goals_diff
        self.pts = pts


def create_standings_object(league_id, standing):
    rank = standing['rank']
    team_id = standing['team_id']
    team_name = standing['teamName']
    team_logo = standing['logo']
    group = standing['group']
    # forme = standing['forme']
    form = get_form(league_id, team_id)
    status = standing['status']
    description = standing['description']
    all_played = standing['all']['matchsPlayed']
    all_win = standing['all']['win']
    all_draw = standing['all']['draw']
    all_lose = standing['all']['lose']
    all_goals_for = standing['all']['goalsFor']
    all_goals_against = standing['all']['goalsAgainst']
    goals_diff = standing['goalsDiff']
    pts = standing['points']

    return Standing(
        rank,
        team_id,
        team_name,
        team_logo,
        group,
        form,
        status,
        description,
        all_played,
        all_win,
        all_draw,
        all_lose,
        all_goals_for,
        all_goals_against,
        goals_diff,
        pts
    )


    """
    {
  "rank": 1,
  "team_id": 157,
  "teamName": "Bayern Munich",
  "logo": "https://media.api-sports.io/football/teams/157.png",
  "group": "Bundesliga",
  "forme": "WWDDW",
  "status": "same",
  "description": "Promotion - Champions League (Group Stage)",
  "all": {
    "matchsPlayed": 13,
    "win": 9,
    "draw": 3,
    "lose": 1,
    "goalsFor": 39,
    "goalsAgainst": 19
  },
  "home": {
    "matchsPlayed": 6,
    "win": 4,
    "draw": 2,
    "lose": 0,
    "goalsFor": 23,
    "goalsAgainst": 8
  },
  "away": {
    "matchsPlayed": 7,
    "win": 5,
    "draw": 1,
    "lose": 1,
    "goalsFor": 16,
    "goalsAgainst": 11
  },
  "goalsDiff": 20,
  "points": 30,
  "lastUpdate": "2020-12-20"
}
    """

class StandingTable(Table):
    def sort_url(self, col_id, reverse=False):
        pass

    rank = Col('')
    logo = Col('')
    team_name = Col('')
    points = Col('Pts')
    games_played = Col('P')
    wins = Col('W')
    draws = Col('D')
    losses = Col('L')
    goals_for = Col('GF')
    goals_against = Col('GA')
    form = Col('Form')


def get_standings_by_league_id(input):
    # TODO: this is stupid, redo. Find a way to distinct how data should be retrieved (API vs DB vs else)

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


class StandingTableRow(object):
    def __init__(self, rank, logo, team_name, games_played, wins, draws, losses, goals_for, goals_against, points,
                 form):
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


def build_list_of_position_objects(league_id):
    position_objects = []


def get_league_standings(league_id):
    table = get_standings_by_league_id(league_id)
    return table


def build_standings_table(league_id):
    table_data = get_league_standings(league_id)

    standing_table_rows = []
    for row in table_data:
        standing_table_rows.append(create_standings_object(league_id, row))
        # logo = row['logo']
        # rank = row['rank']
        # team_name = row['teamName']
        # all_games_stats = row['all']
        # games_played = all_games_stats['matchsPlayed']
        # wins = all_games_stats['win']
        # draws = all_games_stats['draw']
        # losses = all_games_stats['lose']
        # goals_for = all_games_stats['goalsFor']
        # goals_against = all_games_stats['goalsAgainst']
        # points = row['points']
        # form = row['forme']
        #
        # standing_table_rows.append(
        #     StandingTableRow(rank, Markup('<img src =' + logo + ' style="width:20px;height:20px;">'), team_name,
        #                      games_played, wins, draws, losses, goals_for, goals_against, points, form))
    return standing_table_rows


def get_form(league_id, team_id):

    fixtures = get_form_by_team(league_id, team_id)
    fs = build_list_of_fixture_objects(fixtures)

    return fs
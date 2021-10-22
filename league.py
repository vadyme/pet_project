import api_client

# available_leagues = {'segunda_division': 2847,
#                      'championship': 2794,
#                      'bundesliga_1': 2755,
#                      'primera_division': 2833,
#                      'serie_a': 2857,
#                      'premier_league': 2790,
#                      'jupiler_pro_league': 3450,
#                      'super_lig': 2816,
#                      'ucl': 2771,
#                      'uel': 2777
#                      }

available_leagues = {'segunda_division': 3516,
                     'championship': 3501,
                     'bundesliga_1': 3510,
                     'primera_division': 3513,
                     'serie_a': 3576,
                     'premier_league': 3456,
                     'jupiler_pro_league': 3450,
                     'super_lig': 3552,
                    'primeira_liga': 3575,
                     'ucl': 3431,
                     'uel': 3632
                     }


def map_league_name_to_id(league_name):
    if league_name in available_leagues:
        return available_leagues.get(league_name)
    else:
        return None


def urlify_league_name(league_name):
    return league_name.lower().replace(' ', '_')


def get_list_of_matchdays(league_id):
    return api_client.get_rounds_by_league(league_id)['api']['fixtures']
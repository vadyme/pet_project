available_leagues = {'deu_bundesliga': 2755, 'esp_primera': 2833, 'ita_serie_a': 2857, 'eng_premiere_league': 2790}


def map_league_name_to_id(league_name):
    if league_name in available_leagues:
        return available_leagues.get(league_name)
    else:
        return None
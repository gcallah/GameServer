"""
This module encapsulates details about games.
"""
import gamedb.db_connect as dbc
import gamedb.char_types as ctyp

TEST_GAME_NAME = 'Test game'
NAME = 'name'
NUM_PLAYERS = 'num_players'
LEVEL = 'level'
VIOLENCE = 'violence'

TEST_CHAR_NAME = 'Test character'
TEST_CHAR_TYPE = 'Warrior'

TEST_MAP = {
    'graph': {'test loc 1': ['test loc 2'], 'test loc 2': ['test loc 1']},
    'locations': {
        'test loc 1': {
            'description': 'test location 1',
            'actions': ['test item 1', 'test item 2']
        },
        'test loc 2': {
            'description': 'test location 2',
            'actions': ['test item 3', 'test item 4']
        }
    },
    'start': 'test start location',
    'current': 'test start location'
}

# We expect the game database to change frequently:
# For now, we will consider NUM_PLAYERS and LEVEL to be
# our mandatory fields.
REQUIRED_FLDS = [NUM_PLAYERS, LEVEL, VIOLENCE]
GAME_KEY = 'name'
GAMES_COLLECT = 'games'

CHARACTER_KEY = 'characters'
CHARACTER_NAME = 'name'
CHARACTER_TYPE = 'type'

MAP_KEY = 'map'


def get_game_details(name):
    return dbc.fetch_one(GAMES_COLLECT, {GAME_KEY: name})


def game_exists(name):
    """
    Returns whether or not a game exists.
    """
    return get_game_details(name) is not None


def get_games_dict():
    """
    Returns a dictionary of games without revealing game characters.
    """
    # remove game characters from the dictionary
    ret = dbc.fetch_all_as_dict(GAME_KEY, GAMES_COLLECT)
    if ret is not None:
        for game in ret.values():
            if CHARACTER_KEY in game:
                del game[CHARACTER_KEY]
            if MAP_KEY in game:
                del game[MAP_KEY]
    return ret


def get_games():
    return dbc.fetch_all(GAMES_COLLECT)


def add_game(name, details):
    doc = details
    if not isinstance(name, str):
        raise TypeError(f'Wrong type for name: {type(name)=}')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    for field in REQUIRED_FLDS:
        if field not in details:
            raise ValueError(f'Required {field=} missing from details.')
    doc[GAME_KEY] = name
    return dbc.insert_one(GAMES_COLLECT, doc)


def del_game(name):
    return dbc.del_one(GAMES_COLLECT, {GAME_KEY: name})


def add_character(name, char_name, char_type):
    """
    This will add an character to the game specified.
    """
    if not isinstance(char_name, str):
        raise TypeError(f'Wrong type for character name: {type(char_name)=}')
    if not game_exists(name):
        raise ValueError(f'{name} does not exist.')
    if not isinstance(char_type, str):
        raise TypeError(f'Wrong type for character type: {type(char_type)=}')
    if not ctyp.exists(char_type):
        raise ValueError(f'{char_type} does not exist.')
    return dbc.append_to_list(GAMES_COLLECT,
                              GAME_KEY, name,
                              CHARACTER_KEY,
                              {CHARACTER_NAME: char_name,
                               CHARACTER_TYPE: char_type})


def del_character(name, char_name):
    """
    This will delete an character from the game specified.
    """
    if not isinstance(char_name, str):
        raise TypeError(f'Wrong type for character name: {type(char_name)=}')
    if not game_exists(name):
        raise ValueError(f'{name} does not exist.')
    return dbc.pull_from_list(GAMES_COLLECT,
                              GAME_KEY, name,
                              CHARACTER_KEY,
                              {CHARACTER_NAME: char_name})


def game_character_exists(name, char_name):
    """
    Returns whether or not a character exists in a game.
    """
    ret = get_game_details(name)
    if ret is None:
        return False
    if CHARACTER_KEY not in ret:
        return False
    characters = ret[CHARACTER_KEY]
    return characters is not None and \
        any(char[CHARACTER_NAME] == char_name for char in characters)


def add_map(name, map):
    """
    This will add a map to the game specified.
    """
    if not game_exists(name):
        raise ValueError(f'{name} does not exist.')
    if not isinstance(map, dict):
        raise TypeError(f'Wrong type for map: {type(map)=}')
    if len(map['graph']) == 0 or \
        len(map['locations']) == 0 or \
            len(map['graph']) != len(map['locations']):
        raise ValueError('Wrong value for map.')
    for location in [*map['graph']]:
        if location not in [*map['locations']]:
            raise ValueError(f'{location} not in locations.')
    return dbc.update_one(GAMES_COLLECT,
                          {GAME_KEY: name},
                          {'$set': {'map': map}})


def del_map(name):
    """
    This will delete a map from the game specified.
    """
    if not game_exists(name):
        raise ValueError(f'{name} does not exist.')
    return dbc.update_one(GAMES_COLLECT,
                          {GAME_KEY: name},
                          {'$unset': {'map': ""}})


def game_map_exists(name):
    """
    Returns whether or not a map exists in a game.
    """
    ret = get_game_details(name)
    if ret is None:
        return False
    return 'map' in ret


def main():
    print('Getting games as a list:')
    games = get_games()
    print(f'{games=}')
    print('Getting games as a dict:')
    games = get_games_dict()
    print(f'{games=}')
    print(f'{get_game_details(TEST_GAME_NAME)=}')


if __name__ == '__main__':
    main()

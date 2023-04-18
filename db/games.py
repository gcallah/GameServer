"""
This module encapsulates details about games.
"""
import db.db_connect as dbc
import db.char_types as ctyp

TEST_GAME_NAME = 'Test game'
NAME = 'name'
NUM_PLAYERS = 'num_players'
LEVEL = 'level'
VIOLENCE = 'violence'

# We expect the game database to change frequently:
# For now, we will consider NUM_PLAYERS and LEVEL to be
# our mandatory fields.
REQUIRED_FLDS = [NUM_PLAYERS, LEVEL, VIOLENCE]
GAME_KEY = 'name'
GAMES_COLLECT = 'games'

CHARACTER_KEY = 'characters'
CHARACTER_NAME = 'name'
CHARACTER_TYPE = 'type'


def get_game_details(name):
    return dbc.fetch_one(GAMES_COLLECT, {GAME_KEY: name})


def game_exists(name):
    """
    Returns whether or not a game exists.
    """
    return get_game_details(name) is not None


def get_games_dict():
    return dbc.fetch_all_as_dict(GAME_KEY, GAMES_COLLECT)


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


def add_characters(name, char_name, char_type):
    """
    This will add an character to the game specified.
    """
    if not game_exists(name):
        raise ValueError(f'{name} does not exist.')
    if not isinstance(char_name, str):
        raise TypeError(f'Wrong type for character name: {type(char_name)=}')
    if not isinstance(char_type, str):
        raise TypeError(f'Wrong type for character type: {type(char_type)=}')
    if not ctyp.exists(char_type):
        raise ValueError(f'{char_type} does not exist.')
    return dbc.append_to_list(GAMES_COLLECT,
                              GAME_KEY, name,
                              CHARACTER_KEY,
                              {CHARACTER_NAME: char_name,
                               CHARACTER_TYPE: char_type})


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

import os

from unittest.mock import patch

import pytest

import gamedb.games as gm


RUNNING_ON_CICD_SERVER = os.environ.get('CI', False)

TEST_DEL_NAME = 'Game to be deleted'


def create_game_details():
    details = {}
    for field in gm.REQUIRED_FLDS:
        details[field] = 2
    return details


@pytest.fixture(scope='function')
def temp_game():
    gm.add_game(gm.TEST_GAME_NAME, create_game_details())
    yield
    gm.del_game(gm.TEST_GAME_NAME)


@pytest.fixture(scope='function')
def new_game():
    return gm.add_game(TEST_DEL_NAME, create_game_details())


def test_del_game(new_game):
    gm.del_game(TEST_DEL_NAME)
    assert not gm.game_exists(TEST_DEL_NAME)


def test_get_games(temp_game):
    gms = gm.get_games()
    assert isinstance(gms, list)
    assert len(gms) > 0


def test_get_games_dict(temp_game):
    gms = gm.get_games_dict()
    assert isinstance(gms, dict)
    assert len(gms) > 0


def test_get_game_details(temp_game):
    gm_dtls = gm.get_game_details(gm.TEST_GAME_NAME)
    assert isinstance(gm_dtls, dict)


def test_game_exists(temp_game):
    assert gm.game_exists(gm.TEST_GAME_NAME)


def test_game_not_exists():
    assert not gm.game_exists('Surely this is not a game name!')


def test_add_wrong_name_type():
    with pytest.raises(TypeError):
        gm.add_game(7, {})


def test_add_wrong_details_type():
    with pytest.raises(TypeError):
        gm.add_game('a new game', [])


def test_add_missing_field():
    with pytest.raises(ValueError):
        gm.add_game('a new game', {'foo': 'bar'})


def test_add_game():
    gm.add_game(gm.TEST_GAME_NAME, create_game_details())
    assert gm.game_exists(gm.TEST_GAME_NAME)
    gm.del_game(gm.TEST_GAME_NAME)


@patch('gamedb.char_types.exists', return_value=True)
def add_char(mock_exists):
    gm.add_character(gm.TEST_GAME_NAME, gm.TEST_CHAR_NAME, 'Lizard')  # gm.TEST_CHAR_TYPE)


@pytest.fixture(scope='function')
def temp_game_character(temp_game):
    add_char()
    yield
    gm.del_character(gm.TEST_GAME_NAME, gm.TEST_CHAR_NAME)


def test_game_character_exists(temp_game_character):
    assert gm.game_character_exists(gm.TEST_GAME_NAME, gm.TEST_CHAR_NAME)


def test_game_add_character_wrong_name_type(temp_game):
    with pytest.raises(TypeError):
        gm.add_character(gm.TEST_GAME_NAME, 7, gm.TEST_CHAR_TYPE)


def test_game_add_character_wrong_game_name():
    with pytest.raises(ValueError):
        gm.add_character('Surely this is not a game name!',
                          gm.TEST_CHAR_NAME, gm.TEST_CHAR_TYPE)


def test_game_add_character_wrong_char_type(temp_game):
    with pytest.raises(ValueError):
        gm.add_character(gm.TEST_GAME_NAME,
                          gm.TEST_CHAR_NAME,
                          'Surely this is not a character type!')


@pytest.fixture(scope='function')
def temp_game_map(temp_game):
    gm.add_map(gm.TEST_GAME_NAME, gm.TEST_MAP)
    yield
    gm.del_map(gm.TEST_GAME_NAME)


def test_map_exists(temp_game_map):
    assert gm.game_map_exists(gm.TEST_GAME_NAME)


def test_add_map_wrong_game_name():
    with pytest.raises(ValueError):
        gm.add_map('Surely this is not a game name!', gm.TEST_MAP)


def test_add_map_wrong_map_type(temp_game):
    with pytest.raises(TypeError):
        gm.add_map(gm.TEST_GAME_NAME, 7)


def test_add_map_wrong_map(temp_game):
    with pytest.raises(ValueError):
        gm.add_map(gm.TEST_GAME_NAME, 
        {
            'graph': { 'a': ['b'], 'b': ['a'] },
            'locations': {
                'a': { 'description': 'a description', 'actions': ['test action'] }
            },
            'start': 'a',
            'current': 'a'
        })


@pytest.fixture(scope='function')
def new_game_character(temp_game):
    return gm.add_character(gm.TEST_GAME_NAME, gm.TEST_CHAR_NAME, gm.TEST_CHAR_TYPE)


def test_del_game(new_game_character):
    gm.del_character(gm.TEST_GAME_NAME, gm.TEST_CHAR_NAME)
    assert not gm.game_character_exists(gm.TEST_GAME_NAME, gm.TEST_CHAR_NAME)


@pytest.fixture(scope='function')
def new_game_map(temp_game):
    return gm.add_map(gm.TEST_GAME_NAME, gm.TEST_MAP)


def test_del_game(new_game_map):
    gm.del_map(gm.TEST_GAME_NAME)
    assert not gm.game_map_exists(gm.TEST_GAME_NAME)

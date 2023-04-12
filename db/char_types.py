"""
This module encapsulates details about character type.
"""
import db.db_connect as dbc

WIZARD = 'Wizard'
WARRIOR = 'Warrior'
MAGE = 'Mage'

CHAR_TYPES_KEY = 'name'
CHAR_TYPES_COLLECT = 'char_types'


def add_char_type(name, traits):
    if not isinstance(name, str):
        raise TypeError(f'Wrong type for name: {type(name)=}')
    if not isinstance(traits, dict):
        raise TypeError(f'Wrong type for traits: {type(traits)=}')
    # we want to check required fields here!
    if exists(name):
        raise ValueError(f'Char type exists: {name=}')
    traits[CHAR_TYPES_KEY] = name
    return dbc.insert_one(CHAR_TYPES_COLLECT, traits)


def del_char_type(name):
    """
    We expect this function to return 0 if the character type doesn't exist.
    """
    return dbc.del_one(CHAR_TYPES_COLLECT, {CHAR_TYPES_KEY: name})


def get_char_type_details(char_type):
    return dbc.fetch_one(CHAR_TYPES_COLLECT, {CHAR_TYPES_KEY: char_type})


def exists(name):
    return get_char_type_details(name) is not None


def get_char_type_dict():
    """
    Returns a dictionary of character types.
    """
    return dbc.fetch_all_as_dict(CHAR_TYPES_KEY, CHAR_TYPES_COLLECT)


def get_char_types():
    """
    Returns a list of character types.
    """
    return list(get_char_type_dict().keys())


def main():
    char_types = get_char_types()
    print(char_types)
    return


if __name__ == '__main__':
    main()

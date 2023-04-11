"""
This module encapsulates details about users.
"""
import db.db_connect as dbc

TEST_USER_NAME = 'Test user'
NAME = 'name'
EMAIL = 'email'
FULL_NAME = 'full_name'

# We expect the user database to change frequently:
# For now, we will consider EMAIL to be
# our mandatory fields.
REQUIRED_FLDS = [EMAIL]
# users = {TEST_USER_NAME: {EMAIL: 'x@y.com', FULL_NAME: 'Porgy Tirebiter'},
#          'handle': {EMAIL: 'z@y.com', FULL_NAME: 'Nick Danger'}}

USERS_KEY = 'name'
USERS_COLLECT = 'users'

def user_exists(name):
    """
    Returns whether or not a user exists.
    """
    # return name in users
    return get_user_details(name) is not None


def get_users():
    """
    Returns a list of users.
    """
    return list(get_users_dict().keys())


def get_users_dict():
    """
    Returns a dictionary of users.
    """
    dbc.connect_db()
    return dbc.fetch_all_as_dict(USERS_KEY, USERS_COLLECT)

def get_user_details(user):
    return dbc.fetch_one(USERS_COLLECT, {USERS_KEY: user})

def del_user(name):
    return dbc.del_one(USERS_COLLECT, {USERS_KEY: name})

def add_user(name, details):
    if not isinstance(name, str):
        raise TypeError(f'Wrong type for name: {type(name)=}')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    for field in REQUIRED_FLDS:
        if field not in details:
            raise ValueError(f'Required {field=} missing from details.')
    if user_exists(name):
        raise ValueError(f'Char type exists: {name=}')
    details[USERS_KEY] = name
    return dbc.insert_one(USERS_COLLECT, details)


def main():
    users = get_users()
    print(f'{users=}')
    print(f'{get_user_details(TEST_USER_NAME)=}')


if __name__ == '__main__':
    main()

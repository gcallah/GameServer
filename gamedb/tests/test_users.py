import pytest

import gamedb.users as usr

NEW_USER_NAME = 'An absolutely unique username'
DEF_DETAILS = {usr.EMAIL: 'ab@gmail.com', 
               usr.FULL_NAME: 'An absolutely unique username An absolutely unique username'}

def add_user_if_not_there(name, details):
    if not usr.user_exists(name):
        return usr.add_user(name, details)

@pytest.fixture(scope='function')
def temp_user():
    """
    Add a user, then deletes it after the test is run.
    """
    add_user_if_not_there(NEW_USER_NAME, DEF_DETAILS)
    yield
    usr.del_user(NEW_USER_NAME)


@pytest.fixture(scope='function')
def new_user():
    """
    This is used to test deletion, so we don't delete the user at
    the end of the fixture.
    """
    add_user_if_not_there(NEW_USER_NAME, DEF_DETAILS)


def test_get_users(temp_user):
    usrs = usr.get_users()
    assert isinstance(usrs, list)
    assert len(usrs) > 0


def test_get_users_dict(temp_user):
    usrs = usr.get_users_dict()
    assert isinstance(usrs, dict)
    assert len(usrs) > 0


def test_get_user_details(temp_user):
    usr_dets = usr.get_user_details(NEW_USER_NAME)
    assert isinstance(usr_dets, dict)


def test_add_wrong_name_type(temp_user):
    with pytest.raises(TypeError):
        usr.add_user(7, {})


def test_add_wrong_details_type(temp_user):
    with pytest.raises(TypeError):
        usr.add_user('a new user', [])


def test_add_missing_field(temp_user):
    with pytest.raises(ValueError):
        usr.add_user('a new user', {'foo': 'bar'})

def test_add_usr_dup(temp_user):
    """
    See if we catch adding a duplicate user.
    """
    with pytest.raises(ValueError):
        usr.add_user(NEW_USER_NAME, DEF_DETAILS)

def test_user_exists(temp_user):
    assert usr.user_exists(NEW_USER_NAME)

def test_user_type_not_exists():
    assert not usr.user_exists('Some nonsense user name')

def test_del_user(new_user):
    usr.del_user(NEW_USER_NAME)
    assert not usr.user_exists(NEW_USER_NAME)

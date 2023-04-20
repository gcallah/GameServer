import pytest

import gamedb.char_types as ctyp

NEW_CHAR_TYPE = 'Test character type!'
DEF_TRAITS = {'health': 7, 'magic': 10}


def add_char_if_not_there(char_type, traits):
    if not ctyp.exists(char_type):
        return ctyp.add_char_type(char_type, traits)


@pytest.fixture(scope='function')
def temp_char_type():
    """
    Add a character type, then deletes it after the test is run.
    """
    add_char_if_not_there(NEW_CHAR_TYPE, DEF_TRAITS)
    # yield is where the test is run!
    yield
    ctyp.del_char_type(NEW_CHAR_TYPE)


@pytest.fixture(scope='function')
def new_char_type():
    """
    This is used to test deletion, so we don't delete the new character type at
    the end of the fixture.
    """
    add_char_if_not_there(NEW_CHAR_TYPE, DEF_TRAITS)


def test_get_char_types(temp_char_type):
    ct = ctyp.get_char_types()
    assert isinstance(ct, list)
    assert len(ct) > 0


def test_get_char_type_details(temp_char_type):
    ctd = ctyp.get_char_type_details(NEW_CHAR_TYPE)
    assert isinstance(ctd, dict)


def test_add_char_type(temp_char_type):
    assert ctyp.exists(NEW_CHAR_TYPE)


def test_add_char_type_dup(temp_char_type):
    """
    See if we catch adding a duplicate character type.
    """
    with pytest.raises(ValueError):
        ctyp.add_char_type(NEW_CHAR_TYPE, DEF_TRAITS)


def test_exists(temp_char_type):
    assert ctyp.exists(NEW_CHAR_TYPE)


def test_char_type_not_exists():
    assert not ctyp.exists('Some nonsense character type')


def test_del_char_type(new_char_type):
    ctyp.del_char_type(NEW_CHAR_TYPE)
    assert not ctyp.exists(NEW_CHAR_TYPE)

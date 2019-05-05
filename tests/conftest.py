import pytest
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from api.models import DeclBase, Todo

@pytest.fixture(scope='session')
def db_url():
    """Overriding db_url fixture from `nameko_sqlalchemy`

    `db_url` and `model_base` below are used by `db_session` fixture
    from `nameko_sqlalchemy`.

    `db_session` fls
    fixture is used for any database dependent tests.

    For more information see: https://github.com/onefinestay/nameko-sqlalchemy
    """
    url = 'sqlite:///test.db'
    return url

@pytest.fixture(scope="session")
def model_base():
    """Overriding model_base fixture from `nameko_sqlalchemy`"""
    return DeclBase

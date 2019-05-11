""" This conftest file supplies a number of test cases and creates the corresponding Todo Objects to do the corresponding unit tests in test_models.py
"""

from api.models import Todo
from  dateutil.parser import parse
import pytest

test_cases = [('EnglishLesson', parse("2018-05-04 12:00:12")),
              ('FrenchLesson', parse("2019-01-01")),
              (None, parse("2019-01-01")),
              (None, None)]

@pytest.fixture(params = test_cases)
def todo(request):
    """ Pytest fixture to create Todo model instance from each of the test cases
    """
    return Todo(name = request.param[0], date = request.param[1])

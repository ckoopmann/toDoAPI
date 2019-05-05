from api.models import Todo
from  dateutil.parser import parse
import pytest

test_cases = [('EnglishLesson', parse("2018-05-04 12:00:12")),
              ('FrenchLesson', parse("2019-01-01")),
              (None, parse("2019-01-01")),
              (None, None)]

@pytest.fixture(params = test_cases)
def todo(request):
        return Todo(name = request.param[1],
                    date = request.param[1])

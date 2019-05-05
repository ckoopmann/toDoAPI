from api.models import Todo
import dateutil.parser
import pytest

@pytest.fixture(params = [('EnglishLesson', dateutil.parser.parse("2018-05-04 12:00:12")),
                          ('FrenchLesson', dateutil.parser.parse("2019-01-01")),
                          (None, dateutil.parser.parse("2019-01-01")),
                          (None, None)])
def todo(request):
        return Todo(name = request.param[1],
                    date = request.param[1])

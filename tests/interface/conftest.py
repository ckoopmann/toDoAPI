""" This test configuration is largely taken over form the nameko example at: https://github.com/nameko/nameko-examples/blob/master/gateway/test/interface/conftest.py
"""

import pytest
from collections import namedtuple

from nameko.testing.services import replace_dependencies

from api.service import TodoService
import api.models




@pytest.fixture
def config(web_config, rabbit_config, db_url):
    gateway_config = rabbit_config.copy()
    gateway_config.update(web_config)
    gateway_config['DB_URIS'] = {'TodoService:Base': db_url}
    return gateway_config


@pytest.fixture
def create_service_meta(container_factory, config):
    """ Returns a convenience method for creating service test instance

    `container_factory` is a Nameko's test fixture
    for creating service container
    """
    def create(*dependencies, **dependency_map):
        """ Create service instance with specified dependencies mocked

        Dependencies named in *dependencies will be replaced with a
        `MockDependencyProvider`, which injects a `MagicMock` instead of the
        dependency.

        Alternatively, you may use `dependency_map` keyword arguments
        to name a dependency and provide the replacement value that
        the `MockDependencyProvider` should inject.

        For more information read:
        https://github.com/onefinestay/nameko/blob/master/nameko/testing/services.py#L325
        """
        dependency_names = list(dependencies) + list(dependency_map.keys())

        ServiceMeta = namedtuple(
            'ServiceMeta', ['container'] + dependency_names
        )
        container = container_factory(TodoService, config)

        mocked_dependencies = replace_dependencies(
            container, *dependencies, **dependency_map
        )
        if len(dependency_names) == 1:
            mocked_dependencies = (mocked_dependencies, )

        container.start()

        return ServiceMeta(container, *mocked_dependencies, **dependency_map)

    return create


@pytest.fixture
def todo_service(create_service_meta):
    """ Todo service test instance """
    return create_service_meta()

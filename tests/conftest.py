"""Test fixtures to be re-used for different test suites.

Modules in the test suite subdirectories will have access to this
conftest.py, which sets up common functionality for:

* A Harmony Client.
*
"""

import json
import os

import pytest
from harmony import Client, Environment

environment_mapping = {
    'production': Environment.PROD,
    'UAT': Environment.UAT,
}


def pytest_generate_tests(metafunc):
    """Workaround to parametrize pytest functions dynamically.

    This will recognise if the service_collection fixture is included in
    the test function. If so, the `SERVICE_COLLECTIONS` environment variable
    will be parsed into JSON, creating a list of collection objects. The
    test will then be parametrised to run over each element.

    """
    if 'service_collection' in metafunc.fixturenames:
        service_collections = json.loads(os.environ.get('SERVICE_COLLECTIONS', []))
        metafunc.parametrize('service_collection', service_collections)


@pytest.fixture(scope='session')
def harmony_client():
    """A harmony-py Client object for making requests."""
    environment_string = os.environ.get('EARTHDATA_ENVIRONMENT')
    edl_user = os.environ.get('EDL_USER')
    edl_password = os.environ.get('EDL_PASSWORD')
    return Client(
        auth=(edl_user, edl_password), env=environment_mapping.get(environment_string)
    )


@pytest.fixture(scope='session')
def test_output_file():
    """The path to where the failed test information should be written."""
    test_directory = os.environ.get('TEST_DIRECTORY')
    return f'{test_directory}/test_output.json'


@pytest.fixture(scope='session')
def failed_tests(test_output_file):
    """A fixture to accumulate failed test results."""
    failed_test_information = []
    yield failed_test_information
    with open(test_output_file, 'w', encoding='utf-8') as file_handler:
        json.dump(failed_test_information, file_handler, indent=2)

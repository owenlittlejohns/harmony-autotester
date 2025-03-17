"""A module to retrieve the directory containing tests to run for a given service.

The resulting directory will be written to GitHub environment variables as
`test_directory`. If there is no available test suite for the specified UMM-S
record, this module will not create an environment variable.

To enable a test suite to be run, please add to the `PRODUCTION_SERVICE_MAPPING`
and/or `UAT_SERVICE_MAPPING` as appropriate.

See `README.md` for full guidance on configuring a set of tests for a service.

"""

import os

PRODUCTION_SERVICE_MAPPING = {
    'S2697183066-XYZ_PROV': 'tests/hybig',
}
UAT_SERVICE_MAPPING = {
    'S1257776354-EEDTEST': 'tests/hybig',
}


def get_service_test_directory(service_concept_id: str) -> str | None:
    """Get test directory from environment service mapping."""
    earthdata_environment = os.environ.get('EARTHDATA_ENVIRONMENT')

    if earthdata_environment == 'UAT':
        service_mapping = UAT_SERVICE_MAPPING
    else:
        service_mapping = PRODUCTION_SERVICE_MAPPING

    return service_mapping.get(service_concept_id)


def output_service_test_directory(service_test_directory: str) -> None:
    """Write name of service test directory to an environment variable."""
    with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as file_handler:
        print(f'test_directory={service_test_directory}', file=file_handler)


if __name__ == '__main__':
    """Identify test directory for service and write to environment variable."""
    service_concept_id = os.environ.get('SERVICE_CONCEPT_ID')
    service_test_directory = get_service_test_directory(service_concept_id)

    if service_test_directory is not None:
        output_service_test_directory(service_test_directory)

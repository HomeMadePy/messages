"""reusable testing fixtures."""

import os
import pytest

import jsonconfig


##############################################################################
# Travis CI fixtures
##############################################################################

# skip this test if on travs-ci
travis = pytest.mark.skipif("TRAVIS" in os.environ and
                    os.environ["TRAVIS"] == "true",
                    reason='skipping test if on travis-ci')


# skip this test if NOT on travis-ci
not_travis = pytest.mark.skipif("TRAVIS" not in os.environ,
                    reason='skipping test if not on travis-ci')


##############################################################################
# jsonconfig fixtures
##############################################################################

class ConfigMock:
    """Mock class to return instead of jsonconfig.Config."""
    data = {'tester': 'this is a mock'}
    filename = '/default/path'
    pwd = {'myProf_email': None}
    kwargs = {'dump': {'indent': 4}}


@pytest.fixture()
def cfg_mock(monkeypatch):
    """Patches the context manager call `with jsonconfig.Config...`."""
    def enter(param1):
        return ConfigMock()

    def exit(param1, param2, param3, param4):
        pass

    monkeypatch.setattr(jsonconfig.Config, '__enter__', enter)
    monkeypatch.setattr(jsonconfig.Config, '__exit__', exit)

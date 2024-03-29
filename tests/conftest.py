"""reusable testing fixtures."""

import os
from unittest.mock import MagicMock

import pytest


##############################################################################
# Travis CI fixtures
##############################################################################

# skip this test if on travs-ci
skip_if_on_travisCI = pytest.mark.skipif("TRAVIS" in os.environ and
                    os.environ["TRAVIS"] == "true",
                    reason='skipping test if on travis-ci')


# skip this test if NOT on travis-ci
skip_if_not_on_travisCI = pytest.mark.skipif("TRAVIS" not in os.environ,
                    reason='skipping test if not on travis-ci')


##############################################################################
# AsyncIO fixtures
##############################################################################

class AsyncMock(MagicMock):
    """Generic mock class to be used for async testing."""
    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)

from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


INITIAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture
def api_client():
    activities.clear()
    activities.update(deepcopy(INITIAL_ACTIVITIES))

    try:
        with TestClient(app) as client:
            yield client
    finally:
        activities.clear()
        activities.update(deepcopy(INITIAL_ACTIVITIES))
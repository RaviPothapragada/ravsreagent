import os
import pytest
import requests


@pytest.mark.smoke
def test_root_returns_200():
    """Smoke test: hits APP_URL and expects a 200 response at root path.

    Requires the environment variable APP_URL to be set, otherwise the test is skipped.
    """
    app_url = os.environ.get("APP_URL")
    if not app_url:
        pytest.skip("APP_URL not set; skipping smoke test")

    resp = requests.get(app_url, timeout=10)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text[:200]}"


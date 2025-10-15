import os
import pytest
import requests


@pytest.mark.smoke
def test_health_endpoint():
    """Check a health endpoint. Environment variables:
    - APP_URL (required)
    - HEALTH_PATH (optional, default '/health')
    - HEALTH_EXPECT (optional, substring expected in body)
    """
    app_url = os.environ.get("APP_URL")
    if not app_url:
        pytest.skip("APP_URL not set; skipping health test")

    path = os.environ.get("HEALTH_PATH", "/health")
    expect = os.environ.get("HEALTH_EXPECT")

    url = app_url.rstrip("/") + path
    resp = requests.get(url, timeout=10)
    assert resp.status_code == 200, f"Health endpoint {url} returned {resp.status_code}"
    if expect:
        assert expect in resp.text, f"Expected to find '{expect}' in health response"

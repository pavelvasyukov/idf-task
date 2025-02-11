import json
import time
import pytest
from unittest.mock import patch, MagicMock
import requests
from main import fetch_data, save_to_clickhouse

@pytest.fixture
def mock_get():
    """Fixture to mock requests.get"""
    with patch("main.requests.get") as mock:
        yield mock

@pytest.fixture
def mock_clickhouse():
    """Fixture to mock ClickHouse client"""
    with patch("main.clickhouse_connect.get_client") as mock:
        yield mock

# -------------------- TESTS FOR fetch_data --------------------

def test_fetch_data_success(mock_get):
    """Test fetch_data when response is successful (HTTP 200)."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"people": [{"name": "John Doe"}]}

    result = fetch_data("http://example.com")
    assert result == json.dumps({"people": [{"name": "John Doe"}]})


def test_fetch_data_json_error(mock_get):
    """Test fetch_data when response is not valid JSON."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.side_effect = json.JSONDecodeError("Error", "doc", 0)

    result = fetch_data("http://example.com")
    assert result is None


def test_fetch_data_http_429_retry_after(mock_get):
    """Test fetch_data when HTTP 429 is received with Retry-After header."""
    mock_get.side_effect = [
        MagicMock(status_code=429, headers={"Retry-After": "1"}),
        MagicMock(status_code=200, json=lambda: {"success": True}),
    ]

    result = fetch_data("http://example.com")
    assert result == json.dumps({"success": True})


def test_fetch_data_http_500_retry(mock_get):
    """Test fetch_data when HTTP 500 is received (server error)."""
    mock_get.side_effect = [
        MagicMock(status_code=500),
        MagicMock(status_code=200, json=lambda: {"data": "ok"}),
    ]

    result = fetch_data("http://example.com")
    assert result == json.dumps({"data": "ok"})


def test_fetch_data_http_400_fail(mock_get):
    """Test fetch_data when HTTP 400 (client error) is received."""
    mock_get.return_value.status_code = 400
    mock_get.return_value.text = "Bad Request"

    result = fetch_data("http://example.com")
    assert result is None


# -------------------- TESTS FOR save_to_clickhouse --------------------

def test_save_to_clickhouse_success(mock_clickhouse):
    """Test successful data insertion into ClickHouse."""
    mock_instance = mock_clickhouse.return_value
    mock_instance.insert.return_value = None

    save_to_clickhouse('{"data": "test"}')

    mock_clickhouse.assert_called_once()
    mock_instance.insert.assert_called_once_with("RAW_TABLE", [('{"data": "test"}',)])


def test_save_to_clickhouse_connection_fail(mock_clickhouse, caplog):
    """Test ClickHouse connection failure."""
    mock_clickhouse.side_effect = Exception("Connection failed")

    save_to_clickhouse('{"data": "test"}')

    assert "Error while working with ClickHouse: Connection failed" in caplog.text

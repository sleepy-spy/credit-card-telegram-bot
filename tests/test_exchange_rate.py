import pytest
from unittest.mock import patch, Mock
from src.exchange_rate import get_exchange_rate, _cache


@pytest.fixture(autouse=True)
def clear_cache():
    _cache.clear()
    yield
    _cache.clear()


@patch("src.exchange_rate.httpx.get")
def test_fetches_exchange_rate(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"conversion_rate": 1.35}
    mock_get.return_value = mock_response

    rate = get_exchange_rate("usd")
    assert rate == 1.35


@patch("src.exchange_rate.httpx.get")
def test_caches_exchange_rate(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"conversion_rate": 1.35}
    mock_get.return_value = mock_response

    get_exchange_rate("usd")
    get_exchange_rate("usd")
    assert mock_get.call_count == 1


@patch("src.exchange_rate.httpx.get")
def test_different_currencies_cached_separately(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"conversion_rate": 1.35}
    mock_get.return_value = mock_response

    get_exchange_rate("usd")
    get_exchange_rate("eur")
    assert mock_get.call_count == 2


@patch("src.exchange_rate.httpx.get")
def test_builds_correct_url(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"conversion_rate": 1.35}
    mock_get.return_value = mock_response

    get_exchange_rate("usd")
    call_url = mock_get.call_args[0][0]
    assert "pair/USD/SGD" in call_url

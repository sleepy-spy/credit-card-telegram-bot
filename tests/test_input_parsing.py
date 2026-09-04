import pytest
from src.parser import parse_input
from src.card import Card


def test_shop_with_plain_amount():
    result = parse_input("Fairprice 45 sgd")
    assert result["action"] == "recommend_card"
    assert result["shop"] == "fairprice"
    assert result["amount"] == 45.0
    assert result["currency"] == "sgd"


def test_shop_with_multi_word_name():
    result = parse_input("Cold Storage 45 usd")
    assert result["action"] == "recommend_card"
    assert result["shop"] == "cold storage"
    assert result["amount"] == 45.0
    assert result["currency"] == "usd"


def test_add_location():
    result = parse_input("add location Fairprice 5411")
    assert result["action"] == "add_location"
    assert result["shop"] == "fairprice"
    assert result["mcc"] == "5411"


def test_delete_location():
    result = parse_input("delete location Fairprice")
    assert result["action"] == "delete_location"
    assert result["shop"] == "fairprice"


def test_unknown_input():
    result = parse_input("random nonsense")
    assert result["action"] == "unknown"


def test_valid_card():
    result = parse_input("UOB PRVI Miles")
    assert result["action"] == "show_limits"
    assert isinstance(result["card"], Card)
    assert result["card"].get_name() == "UOB PRVI Miles"


def test_invalid_card():
    result = parse_input("Fake Card Name")
    assert result["action"] == "unknown"


# --- New Tests ---


def test_recommend_card_requires_currency():
    result = parse_input("Fairprice 45")
    assert result["action"] == "unknown"


def test_recommend_card_float_amount():
    result = parse_input("Fairprice 9.99 sgd")
    assert result["action"] == "recommend_card"
    assert result["amount"] == 9.99


def test_currency_lowercased():
    result = parse_input("Fairprice 45 SGD")
    assert result["currency"] == "sgd"


def test_add_location_multi_word_shop():
    result = parse_input("add location Cold Storage 5411")
    assert result["action"] == "add_location"
    assert result["shop"] == "cold storage"
    assert result["mcc"] == "5411"


def test_show_limits_case_insensitive():
    result = parse_input("uob prvi miles")
    assert result["action"] == "show_limits"
    assert isinstance(result["card"], Card)

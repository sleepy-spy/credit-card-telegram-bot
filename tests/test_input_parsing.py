import pytest
from src.parser import parse_input


def test_shop_with_plain_amount():
    result = parse_input("Fairprice 45")
    assert result["action"] == "recommend_card"
    assert result["shop"] == "fairprice"
    assert result["amount"] == 45


def test_shop_with_multi_word_name():
    result = parse_input("Cold Storage 45")
    assert result["action"] == "recommend_card"
    assert result["shop"] == "cold storage"
    assert result["amount"] == 45


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
    result = parse_input("UOB Prvi Miles")
    assert result["action"] == "show_limits"
    assert result["card"] == "uob prvi miles"


def test_valid_card_case_insensitive():
    result = parse_input("HSBC Revolution")
    assert result["action"] == "show_limits"
    assert result["card"] == "hsbc revolution"


def test_invalid_card():
    result = parse_input("Fake Card Name")
    assert result["action"] == "unknown"

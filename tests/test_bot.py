import pytest
from unittest.mock import Mock, patch
from src.bot import (
    route_message,
    handle_recommend_card,
    handle_show_limits,
    handle_add_location,
    handle_delete_location,
    handle_unknown,
)


@pytest.fixture
def mock_update():
    update = Mock()
    update.message = Mock()
    update.message.text = ""
    return update


@pytest.fixture
def mock_context():
    return Mock()


# --- Router Tests ---


@patch("src.bot.handle_recommend_card")
@patch("src.bot.parse_input")
def test_routes_to_recommend_card(mock_parse, mock_handler, mock_update, mock_context):
    mock_parse.return_value = {"action": "recommend_card", "shop": "fairprice", "amount": 45, "currency": "sgd"}
    route_message(mock_update, mock_context)
    mock_handler.assert_called_once_with(mock_update, "fairprice", 45, "sgd")


@patch("src.bot.handle_show_limits")
@patch("src.bot.parse_input")
def test_routes_to_show_limits(mock_parse, mock_handler, mock_update, mock_context):
    mock_parse.return_value = {"action": "show_limits", "card": "uob prvi miles"}
    route_message(mock_update, mock_context)
    mock_handler.assert_called_once_with(mock_update, "uob prvi miles")


@patch("src.bot.handle_add_location")
@patch("src.bot.parse_input")
def test_routes_to_add_location(mock_parse, mock_handler, mock_update, mock_context):
    mock_parse.return_value = {"action": "add_location", "shop": "fairprice", "mcc": "5411"}
    route_message(mock_update, mock_context)
    mock_handler.assert_called_once_with(mock_update, "fairprice", "5411")


@patch("src.bot.handle_delete_location")
@patch("src.bot.parse_input")
def test_routes_to_delete_location(mock_parse, mock_handler, mock_update, mock_context):
    mock_parse.return_value = {"action": "delete_location", "shop": "fairprice"}
    route_message(mock_update, mock_context)
    mock_handler.assert_called_once_with(mock_update, "fairprice")


@patch("src.bot.handle_unknown")
@patch("src.bot.parse_input")
def test_routes_to_unknown(mock_parse, mock_handler, mock_update, mock_context):
    mock_parse.return_value = {"action": "unknown"}
    route_message(mock_update, mock_context)
    mock_handler.assert_called_once_with(mock_update)


# --- Handler Tests ---


def test_recommend_card_replies_with_card(mock_update):
    handle_recommend_card(mock_update, "fairprice", 45, "sgd")
    mock_update.message.reply_text.assert_called_once()


def test_recommend_card_includes_card_name(mock_update):
    handle_recommend_card(mock_update, "fairprice", 45, "sgd")
    call_args = mock_update.message.reply_text.call_args[0][0]
    assert "UOB PRVI Miles" in call_args


def test_recommend_card_includes_reward_amount(mock_update):
    handle_recommend_card(mock_update, "fairprice", 45, "sgd")
    call_args = mock_update.message.reply_text.call_args[0][0]
    assert "63" in call_args


def test_recommend_card_with_different_currency(mock_update):
    handle_recommend_card(mock_update, "fairprice", 20, "usd")
    call_args = mock_update.message.reply_text.call_args[0][0]
    assert "48" in call_args


def test_recommend_card_with_regional_currency(mock_update):
    handle_recommend_card(mock_update, "fairprice", 10, "thb")
    call_args = mock_update.message.reply_text.call_args[0][0]
    assert "30" in call_args


def test_show_limits_replies_with_info(mock_update):
    handle_show_limits(mock_update, "uob prvi miles")
    mock_update.message.reply_text.assert_called_once()


def test_add_location_replies_with_confirmation(mock_update):
    handle_add_location(mock_update, "fairprice", "5411")
    mock_update.message.reply_text.assert_called_once()


def test_delete_location_replies_with_confirmation(mock_update):
    handle_delete_location(mock_update, "fairprice")
    mock_update.message.reply_text.assert_called_once()


def test_unknown_replies_with_help(mock_update):
    handle_unknown(mock_update)
    mock_update.message.reply_text.assert_called_once()

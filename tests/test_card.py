import pytest
from src.card import Card, UOBPrviMiles


# --- Base Card Tests ---


def test_card_is_abstract():
    with pytest.raises(TypeError):
        Card()


def test_card_has_calculate_reward():
    assert hasattr(UOBPrviMiles, "calculate_reward")


def test_card_has_get_name():
    assert hasattr(UOBPrviMiles, "get_name")


# --- $5 Rounding Tests ---


def test_rounds_down_to_nearest_5():
    card = UOBPrviMiles()
    assert card.round_to_nearest_5(9.99) == 5


def test_exact_5_multiple():
    card = UOBPrviMiles()
    assert card.round_to_nearest_5(10.00) == 10


def test_below_5_returns_zero():
    card = UOBPrviMiles()
    assert card.round_to_nearest_5(4.99) == 0


def test_exactly_5():
    card = UOBPrviMiles()
    assert card.round_to_nearest_5(5.00) == 5


def test_large_amount():
    card = UOBPrviMiles()
    assert card.round_to_nearest_5(47.99) == 45


def test_zero_amount():
    card = UOBPrviMiles()
    assert card.round_to_nearest_5(0) == 0


# --- $1 Rounding Tests ---


def test_round_to_nearest_1_whole_number():
    card = UOBPrviMiles()
    assert card.round_to_nearest_1(10.00) == 10


def test_round_to_nearest_1_decimal():
    card = UOBPrviMiles()
    assert card.round_to_nearest_1(9.99) == 9


def test_round_to_nearest_1_below_1():
    card = UOBPrviMiles()
    assert card.round_to_nearest_1(0.99) == 0


def test_round_to_nearest_1_exactly_1():
    card = UOBPrviMiles()
    assert card.round_to_nearest_1(1.00) == 1


def test_round_to_nearest_1_zero():
    card = UOBPrviMiles()
    assert card.round_to_nearest_1(0) == 0


# --- Currency/Region Rate Tests ---


def test_local_sgd():
    card = UOBPrviMiles()
    assert card._get_rate("sgd") == 1.4


def test_overseas_usd():
    card = UOBPrviMiles()
    assert card._get_rate("usd") == 2.4


def test_overseas_eur():
    card = UOBPrviMiles()
    assert card._get_rate("eur") == 2.4


def test_regional_idr():
    card = UOBPrviMiles()
    assert card._get_rate("idr") == 3.0


def test_regional_myr():
    card = UOBPrviMiles()
    assert card._get_rate("myr") == 3.0


def test_regional_thb():
    card = UOBPrviMiles()
    assert card._get_rate("thb") == 3.0


def test_regional_vnd():
    card = UOBPrviMiles()
    assert card._get_rate("vnd") == 3.0


# --- Excluded MCC Tests ---


def test_excluded_mcc_4829():
    card = UOBPrviMiles()
    assert card.calculate_reward("4829", "sgd", 100) == 0


def test_excluded_mcc_7995():
    card = UOBPrviMiles()
    assert card.calculate_reward("7995", "sgd", 100) == 0


def test_excluded_mcc_6012():
    card = UOBPrviMiles()
    assert card.calculate_reward("6012", "sgd", 100) == 0


def test_excluded_mcc_9311():
    card = UOBPrviMiles()
    assert card.calculate_reward("9311", "sgd", 100) == 0


def test_valid_mcc_5411():
    card = UOBPrviMiles()
    assert card.calculate_reward("5411", "sgd", 100) > 0


# --- Full Calculation Tests ---


def test_local_valid_mcc():
    card = UOBPrviMiles()
    # $10 SGD, MCC 5411 (valid), rate 1.4
    assert card.calculate_reward("5411", "sgd", 10) == 14


def test_overseas_valid_mcc():
    card = UOBPrviMiles()
    # $10 USD, MCC 5411 (valid), rate 2.4
    assert card.calculate_reward("5411", "usd", 10) == 24


def test_regional_valid_mcc():
    card = UOBPrviMiles()
    # $10 IDR, MCC 5411 (valid), rate 3.0
    assert card.calculate_reward("5411", "idr", 10) == 30


def test_local_with_rounding():
    card = UOBPrviMiles()
    # $9.99 SGD → rounds to $5, rate 1.4 = 7
    assert card.calculate_reward("5411", "sgd", 9.99) == 7


def test_below_5_no_miles():
    card = UOBPrviMiles()
    # $4.99 SGD → rounds to $0
    assert card.calculate_reward("5411", "sgd", 4.99) == 0


def test_overseas_with_rounding():
    card = UOBPrviMiles()
    # $23.99 USD → rounds to $20, rate 2.4 = 48
    assert card.calculate_reward("5411", "usd", 23.99) == 48


def test_regional_with_rounding():
    card = UOBPrviMiles()
    # $14.99 THB → rounds to $10, rate 3.0 = 30
    assert card.calculate_reward("5411", "thb", 14.99) == 30


def test_excluded_mcc_returns_zero_even_with_high_amount():
    card = UOBPrviMiles()
    # MCC 7995 (gambling) excluded
    assert card.calculate_reward("7995", "sgd", 1000) == 0


# --- get_name Tests ---


def test_get_name():
    card = UOBPrviMiles()
    assert card.get_name() == "UOB PRVI Miles"


# --- Foreign Transaction Fee Tests ---


def test_local_skips_fee_check():
    card = UOBPrviMiles()
    assert card.calculate_reward("5411", "sgd", 100) == 140


def test_foreign_regional_below_threshold():
    card = UOBPrviMiles()
    # cost_per_mile = 0.0325 / 3.0 * 100 = 1.08 cents (below 1.5)
    assert card.calculate_reward("5411", "idr", 100) == 300


def test_foreign_other_below_threshold():
    card = UOBPrviMiles()
    # cost_per_mile = 0.0325 / 2.4 * 100 = 1.35 cents (below 1.5)
    assert card.calculate_reward("5411", "usd", 100) == 240


def test_foreign_above_threshold():
    card = UOBPrviMiles()
    original_fee = card.FOREIGN_TX_FEE
    card.FOREIGN_TX_FEE = 0.05
    # cost_per_mile = 0.05 / 2.4 * 100 = 2.08 cents (above 1.5)
    assert card.calculate_reward("5411", "usd", 100) == 0
    card.FOREIGN_TX_FEE = original_fee


def test_foreign_exact_threshold():
    card = UOBPrviMiles()
    original_fee = card.FOREIGN_TX_FEE
    card.FOREIGN_TX_FEE = 0.036
    # cost_per_mile = 0.036 / 2.4 * 100 = 1.5 cents (>= 1.5, return 0)
    assert card.calculate_reward("5411", "usd", 100) == 0
    card.FOREIGN_TX_FEE = original_fee


def test_foreign_just_below_threshold():
    card = UOBPrviMiles()
    original_fee = card.FOREIGN_TX_FEE
    card.FOREIGN_TX_FEE = 0.03599999976
    # cost_per_mile < 1.5, miles awarded
    assert card.calculate_reward("5411", "usd", 100) == 240
    card.FOREIGN_TX_FEE = original_fee

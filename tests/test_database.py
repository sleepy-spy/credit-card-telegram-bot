import pytest
from src.database import init_db, add_shop, delete_shop, get_shop_mcc, get_all_shops


# --- init_db Tests ---


def test_init_db_creates_connection():
    conn = init_db(":memory:")
    assert conn is not None


def test_init_db_creates_shops_table():
    conn = init_db(":memory:")
    result = conn.execute("SELECT * FROM shops").fetchall()
    assert result == []


def test_init_db_is_idempotent():
    conn = init_db(":memory:")
    conn2 = init_db(":memory:")
    assert conn is not None
    assert conn2 is not None


# --- add_shop Tests ---


def test_add_shop_and_get_mcc():
    conn = init_db(":memory:")
    add_shop(conn, "fairprice", "5411")
    result = get_shop_mcc(conn, "fairprice")
    assert result == "5411"


def test_add_shop_replaces_existing():
    conn = init_db(":memory:")
    add_shop(conn, "fairprice", "5411")
    add_shop(conn, "fairprice", "5812")
    result = get_shop_mcc(conn, "fairprice")
    assert result == "5812"


def test_add_multiple_shops():
    conn = init_db(":memory:")
    add_shop(conn, "fairprice", "5411")
    add_shop(conn, "starbucks", "5812")
    assert get_shop_mcc(conn, "fairprice") == "5411"
    assert get_shop_mcc(conn, "starbucks") == "5812"


# --- get_shop_mcc Tests ---


def test_get_shop_mcc_returns_none_for_unknown():
    conn = init_db(":memory:")
    result = get_shop_mcc(conn, "nonexistent")
    assert result is None


def test_get_shop_mcc_case_sensitive():
    conn = init_db(":memory:")
    add_shop(conn, "fairprice", "5411")
    result = get_shop_mcc(conn, "Fairprice")
    assert result is None


# --- delete_shop Tests ---


def test_delete_shop_removes_entry():
    conn = init_db(":memory:")
    add_shop(conn, "fairprice", "5411")
    result = delete_shop(conn, "fairprice")
    assert result is True
    assert get_shop_mcc(conn, "fairprice") is None


def test_delete_shop_returns_false_for_unknown():
    conn = init_db(":memory:")
    result = delete_shop(conn, "fairprice")
    assert result is False


def test_delete_does_not_affect_other_shops():
    conn = init_db(":memory:")
    add_shop(conn, "fairprice", "5411")
    add_shop(conn, "starbucks", "5812")
    delete_shop(conn, "fairprice")
    assert get_shop_mcc(conn, "starbucks") == "5812"


# --- get_all_shops Tests ---


def test_get_all_shops_returns_list():
    conn = init_db(":memory:")
    result = get_all_shops(conn)
    assert isinstance(result, list)


def test_get_all_shops_empty_when_no_shops():
    conn = init_db(":memory:")
    result = get_all_shops(conn)
    assert result == []


def test_get_all_shops_lists_all():
    conn = init_db(":memory:")
    add_shop(conn, "fairprice", "5411")
    add_shop(conn, "starbucks", "5812")
    result = get_all_shops(conn)
    assert len(result) == 2
    assert {"name": "fairprice", "mcc_code": "5411"} in result
    assert {"name": "starbucks", "mcc_code": "5812"} in result

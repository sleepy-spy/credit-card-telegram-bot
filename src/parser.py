EXISTING_CARDS = [
    "uob prvi miles",
    "hsbc revolution",
    "uob krisflyer",
]


def parse_input(user_input: str) -> dict:
    text = user_input.strip().lower().replace("'", "")

    if text.startswith("add location"):
        parts = text.split()
        return {
            "action": "add_location",
            "shop": " ".join(parts[2:-1]),
            "mcc": parts[-1],
        }

    if text.startswith("delete location"):
        shop = text.split(maxsplit=2)[2]
        return {
            "action": "delete_location",
            "shop": shop,
        }

    parts = text.rsplit(maxsplit=1)
    if len(parts) == 2:
        amount_str = parts[1].lstrip("$")
        if amount_str.isdigit():
            return {
                "action": "recommend_card",
                "shop": parts[0],
                "amount": int(amount_str),
            }

    if text in EXISTING_CARDS:
        return {"action": "show_limits", "card": text}

    return {"action": "unknown"}

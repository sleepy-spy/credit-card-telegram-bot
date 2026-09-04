from src.card import Card, CARDS


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

    # [shop] [amount] [currency]
    parts = text.rsplit(maxsplit=2)
    if len(parts) == 3:
        amount_str = parts[1].lstrip("$")
        if amount_str.replace(".", "").isdigit():
            return {
                "action": "recommend_card",
                "shop": parts[0],
                "amount": float(amount_str),
                "currency": parts[2].lower(),
            }

    # Show limits (match by card name)
    for card in CARDS:
        if text == card.get_name().lower():
            return {"action": "show_limits", "card": card}

    return {"action": "unknown"}

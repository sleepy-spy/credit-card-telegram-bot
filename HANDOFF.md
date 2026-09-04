# Handoff Document

## Project Summary
A Telegram bot that recommends the best credit card to use at specific shops based on card rules, shop MCC codes, and spending amounts.

## Tech Stack
- Python 3.13
- SQLite (not yet implemented)
- python-telegram-bot v22.8

## Current State

### Completed
- Project scaffolding (venv, requirements.txt, src/, tests/)
- Input parsing logic (`src/parser.py`) — supports new format `[Shop] [Amount] [Currency]`
- Parser tests (`tests/test_input_parsing.py`) — 13 tests, all passing
- Card class hierarchy (`src/card.py`) — `Card` ABC + `UOBPrviMiles` subclass
- Card tests (`tests/test_card.py`) — 35 tests, all passing
- Bot handler with routing (`src/bot.py`) — `route_message` (sync) + `handle_message` (async wrapper)
- Bot handler tests (`tests/test_bot.py`) — 14 tests, all passing
- Bot token storage via `.env` file
- Telegram bot connection boilerplate (`/start` command, message handler)

### In Progress
- None

### Not Started
- SQLite database for storing shops and MCC codes
- `add location` command — store shop → MCC in database
- `delete location` command — remove shop from database
- Card limit tracking
- Limit tracking tests

## Key Files

| File | Purpose |
|---|---|
| `src/parser.py` | Parses user input, returns action dict with Card objects |
| `src/card.py` | Card ABC + UOBPrviMiles subclass + CARDS list |
| `src/bot.py` | Telegram bot handlers and routing logic |
| `tests/test_input_parsing.py` | Parser tests (13 tests) |
| `tests/test_card.py` | Card class tests (35 tests) |
| `tests/test_bot.py` | Bot handler tests (14 tests) |
| `requirements.txt` | Python dependencies |
| `.env` | Bot token storage (BOT_TOKEN=...) |
| `AGENTS.md` | Project rules and conventions |

## Parser Actions

| Action | Input Format | Output |
|---|---|---|
| `recommend_card` | `[Shop] [Amount] [Currency]` | `{action, shop, amount, currency}` |
| `show_limits` | `[Card Name]` | `{action, card}` (Card object) |
| `add_location` | `add location [Shop] [MCC]` | `{action, shop, mcc}` |
| `delete_location` | `delete location [Shop]` | `{action, shop}` |
| `unknown` | Any other input | `{action: "unknown"}` |

## Existing Cards

| Card | Regional Currencies | Earn Rate (Local) | Earn Rate (Overseas) | Earn Rate (Regional) |
|---|---|---|---|---|
| UOB PRVI Miles | IDR, MYR, THB, VND | 1.4 miles/$1 | 2.4 miles/$1 | 3.0 miles/$1 |

- Cards defined in `src/card.py` as `CARDS` list
- Card class hierarchy: `Card` (ABC) → `UOBPrviMiles`
- Excluded MCCs handled per card
- $5 rounding applied before calculation

## Bot Response Formats
- `/start` → "Welcome! Send me a message like: [Shop] [Amount] [Currency]"
- `recommend_card` → "Best card for {shop} at ${amount} is {card_name} ({miles} miles)"
- `show_limits` → "Card: {card}"
- `add_location` → "Added {shop} with MCC {mcc}"
- `delete_location` → "Deleted {shop}"
- `unknown` → "Unknown command. Type /start for help."

## Architecture

```
Telegram Message
       ↓
handle_message (async, telegram wrapper)
       ↓
route_message (sync, routing logic)
       ↓
parser.py → action dict
       ↓
handler functions (sync)
       ↓
card.py → calculate_reward()
```

## Next Steps
1. Implement SQLite database schema for shops and MCC codes
2. Implement `add location` — store shop → MCC in database
3. Implement `delete location` — remove shop from database
4. Integrate database with `handle_recommend_card` (replace dummy MCC)
5. Implement card limit tracking
6. Add database tests
7. Update HANDOFF.md when complete

## Notes
- This project uses TDD (test-driven development)
- All commits must use conventional commit format
- All source code goes in `src/` folder
- Ask before making decisions not discussed beforehand
- Handlers stay synchronous (only telegram wrapper is async)
- Currency is lowercased (sgd, not SGD)

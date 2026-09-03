# Handoff Document

## Project Summary
A Telegram bot that recommends the best credit card to use at specific shops based on card rules, shop MCC codes, and spending amounts.

## Tech Stack
- Python 3.13
- SQLite
- python-telegram-bot v22.8

## Current State

### Completed
- Project scaffolding (venv, requirements.txt, src/, tests/)
- Input parsing logic (`src/parser.py`)
- Parser tests (`tests/test_input_parsing.py`) — 8 tests, all passing
- Pytest installed and configured

### In Progress
- Telegram bot handler code (`src/bot.py`) — drafted but not yet implemented

### Not Started
- SQLite database for storing cards, shops, MCC codes
- Card limit tracking
- Database integration with bot handlers
- Bot token storage via .env file

## Key Files

| File | Purpose |
|---|---|
| `src/parser.py` | Parses user input, returns action dict |
| `src/__init__.py` | Package marker |
| `tests/test_input_parsing.py` | Tests for parser logic |
| `tests/__init__.py` | Package marker |
| `requirements.txt` | Python dependencies |
| `AGENTS.md` | Project rules and conventions |

## Parser Actions

| Action | Input Format | Output |
|---|---|---|
| `recommend_card` | `[Shop] [Amount]` | `{action, shop, amount}` |
| `show_limits` | `[Card Name]` | `{action, card}` |
| `add_location` | `add location [Shop] [MCC]` | `{action, shop, mcc}` |
| `delete_location` | `delete location [Shop]` | `{action, shop}` |
| `unknown` | Any other input | `{action: "unknown"}` |

## Existing Cards (hardcoded in parser.py)
- uob prvi miles
- hsbc revolution
- uob krisflyer

## Bot Response Formats
- `/start` → "Welcome!"
- `recommend_card` → "Best card for {shop} at ${amount} is [card]"
- `show_limits` → "Card: {card}, Limit: [limit], Amount Spent [amount_spent]"
- `add_location` → "Added {shop} with MCC {mcc}"
- `delete_location` → "Deleted {shop}"
- `unknown` → "Unknown command. Type /start for help."

## Next Steps
1. Implement `src/bot.py` with handler functions
2. Set up SQLite database schema
3. Integrate database with bot handlers
4. Store bot token via .env file
5. Add database tests

## Notes
- This project uses TDD (test-driven development)
- All commits must use conventional commit format
- All source code goes in `src/` folder
- Ask before making decisions not discussed beforehand

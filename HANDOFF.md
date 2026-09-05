# Handoff Document

## Project Summary
A Telegram bot that recommends the best credit card to use at specific shops based on card rules, shop MCC codes, spending amounts, and foreign transaction fees.

## Tech Stack
- Python 3.13
- SQLite
- python-telegram-bot v22.8

## Current State

### Completed
- Project scaffolding (venv, requirements.txt, src/, tests/)
- Input parsing logic (`src/parser.py`) — supports `[Shop] [Amount] [Currency]`
- Parser tests (`tests/test_input_parsing.py`) — 13 tests, all passing
- Card class hierarchy (`src/card.py`) — `Card` ABC + `UOBPrviMiles` subclass
- Card tests (`tests/test_card.py`) — 41 tests, all passing
- Foreign transaction fee check in `calculate_reward` — cards with cost_per_mile >= 1.5¢ return 0 miles
- SQLite database (`src/database.py`) — init_db, add_shop, delete_shop, get_shop_mcc, get_all_shops
- Database tests (`tests/test_database.py`) — 14 tests, all passing
- Exchange rate API integration (`src/exchange_rate.py`) — get_exchange_rate() with in-memory cache
- Exchange rate tests (`tests/test_exchange_rate.py`) — 4 tests, all passing
- Bot handlers with routing (`src/bot.py`) — route_message (sync) + handle_message (async wrapper)
- Bot handler tests (`tests/test_bot.py`) — 18 tests, all passing
- Bot token storage via `~/.env-storage/credit-card-telegram-bot/.env`
- Telegram bot connection boilerplate (`/start` command, message handler)

### In Progress
- Inline keyboard refactor — replacing free-text input with Telegram inline keyboards

### Not Started
- TTL for exchange rate cache (24h expiry)
- Card limit tracking
- Limit tracking tests

## Key Files

| File | Purpose |
|---|---|
| `src/parser.py` | Parses user input, returns action dict with Card objects |
| `src/card.py` | Card ABC + UOBPrviMiles subclass + CARDS list |
| `src/database.py` | SQLite CRUD for shops table |
| `src/exchange_rate.py` | ExchangeRate-API fetch with in-memory cache |
| `src/bot.py` | Telegram bot handlers and routing logic |
| `tests/test_input_parsing.py` | Parser tests (13 tests) |
| `tests/test_card.py` | Card class tests (41 tests) |
| `tests/test_database.py` | Database tests (14 tests) |
| `tests/test_exchange_rate.py` | Exchange rate tests (4 tests) |
| `tests/test_bot.py` | Bot handler tests (18 tests) |
| `requirements.txt` | Python dependencies |
| `~/.env-storage/credit-card-telegram-bot/.env` | Bot token + API key storage |
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

| Card | Regional Currencies | Earn Rate (Local) | Earn Rate (Overseas) | Earn Rate (Regional) | Foreign TX Fee | Cost/Mile Threshold |
|---|---|---|---|---|---|---|
| UOB PRVI Miles | IDR, MYR, THB, VND | 1.4 miles/$1 | 2.4 miles/$1 | 3.0 miles/$1 | 3.25% | 1.5¢ |

- Cards defined in `src/card.py` as `CARDS` list
- Card class hierarchy: `Card` (ABC) → `UOBPrviMiles`
- Excluded MCCs handled per card
- $5 rounding applied before calculation
- Foreign fee check: `cost_per_mile = (FOREIGN_TX_FEE / rate) * 100` — if >= 1.5¢, returns 0 miles

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
       ↓
database.py → get_shop_mcc() (for recommendations)
```

## Next Steps
1. Refactor bot.py to use inline keyboards (see Inline Keyboard Plan below)
2. Write inline keyboard tests first (TDD)
3. Implement inline keyboard handlers
4. Implement TTL for exchange rate cache
5. Implement card limit tracking
6. Add limit tracking tests

---

## Inline Keyboard Plan

### Goal
Replace free-text input with Telegram inline keyboards. User taps buttons instead of typing. Flow: search → see results as buttons → tap to select.

### States

| State | Value | Description |
|---|---|---|
| `CHOOSING` | 0 | Main menu — user sees 4 buttons |
| `TYPING_SHOP_SEARCH` | 1 | User types shop name to search |
| `TYPING_CARD_SEARCH` | 2 | User types card name to search |
| `TYPING_AMOUNT` | 3 | User types spend amount |
| `TYPING_CURRENCY_SEARCH` | 4 | User types currency to search |
| `TYPING_ADD_LOCATION` | 5 | User types shop + MCC |
| `CONFIRMING_ADD` | 6 | Confirm add location |
| `CONFIRMING_DELETE` | 7 | Confirm delete location |
| `ACTION_DONE` | -1 | Return to main menu |

### User Flows

#### Recommend a card
```
/start
  → [Recommend Card] [Check Limits] [Add Location] [Delete Location]
    → User taps [Recommend Card]
      → "Type a shop name to search:"
        → User types "fair"
          → [FairPrice] [FairPrice Finest] [Back]
            → User taps [FairPrice]
              → "How much are you spending?"
                → User types "45"
                  → "Which currency?" + [SGD] [USD] [EUR] [...]
                    → User taps [SGD]
                      → "Best card for FairPrice at $45 SGD: UOB PRVI Miles (63 miles)"
                        → [Main Menu]
```

#### Check limits
```
→ User taps [Check Limits]
  → "Which card?" + [UOB PRVI Miles] [Back]
    → User taps [UOB PRVI Miles]
      → "Card: UOB PRVI Miles"
        → [Main Menu]
```

#### Add location
```
→ User taps [Add Location]
  → "Type shop name and MCC (e.g. fairprice 5411):"
    → User types "fairprice 5411"
      → "Add FairPrice with MCC 5411?" + [Yes] [No]
        → User taps [Yes]
          → "Added FairPrice with MCC 5411"
            → [Main Menu]
```

#### Delete location
```
→ User taps [Delete Location]
  → "Which shop?" + [FairPrice] [Starbucks] [Back]
    → User taps [FairPrice]
      → "Delete FairPrice?" + [Yes] [No]
        → User taps [Yes]
          → "Deleted FairPrice"
            → [Main Menu]
```

### Handlers

| Handler | Trigger | Response | Next State |
|---|---|---|---|
| `start` | `/start` | Welcome + 4 buttons | `CHOOSING` |
| `menu_handler` | Button tap | Routes to flow | Varies |
| `search_shop` | Text in shop search | Shows matching shops as buttons | `TYPING_SHOP_SEARCH` |
| `select_shop` | Shop button tap | Asks for amount | `TYPING_AMOUNT` |
| `enter_amount` | Text (number) | Asks for currency | `TYPING_CURRENCY_SEARCH` |
| `search_currency` | Text in currency search | Shows matching currencies as buttons | `TYPING_CURRENCY_SEARCH` |
| `select_currency` | Currency button tap | Shows recommendation | `ACTION_DONE` |
| `search_card` | Text in card search | Shows matching cards as buttons | `TYPING_CARD_SEARCH` |
| `select_card` | Card button tap | Shows card info | `ACTION_DONE` |
| `enter_add_location` | Text (shop + mcc) | Shows confirmation | `CONFIRMING_ADD` |
| `confirm_add` | Yes button | Calls add_shop | `ACTION_DONE` |
| `confirm_delete` | Yes button | Calls delete_shop | `ACTION_DONE` |
| `cancel` | Cancel/Back button | Returns to main menu | `CHOOSING` |
| `back_to_menu` | Back button | Shows main menu | `CHOOSING` |

### Implementation Order (TDD)
1. Write all tests for inline keyboard handlers
2. Show tests fail
3. Implement handlers
4. Wire up ConversationHandler in main block

### Key Design Decisions
- Use `ConversationHandler` from python-telegram-bot for state management
- `CallbackQueryHandler` for button taps
- `MessageHandler(filters.TEXT)` for text input within states
- `user_data` dict stores intermediate state (shop, card, amount, currency)
- Search results limited to 8 buttons (Telegram limit)
- `parse_input.py` becomes less relevant — inline keyboards handle routing

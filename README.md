# credit-card-telegram-bot

# Purpose
- This telegram bot serves as an easy way to identify what are the best cards to use at specific shops, based on
    - Cards available
    - Card limits
    - Shop you are at
    - Amount paid (due to $5 rounding rules)

# How it works
- Simply open up the bot, and use the following syntax to identify which card should be used
    - [Shop name] [Amount]
- If you want to see your current card limits, and how much you have spent on each card, simply type
    - [Card name]
- If you wish to add a new location, type
    - add location [Shop Name] [MCC]
- If you wish to delete a location, tpe
    - delete location [Shop Name]

# Implementation
## Stack 
- Python 3.13
- SQLite




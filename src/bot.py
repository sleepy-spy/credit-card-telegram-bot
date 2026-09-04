import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from src.parser import parse_input
from src.card import CARDS

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome! Send me a message like: [Shop] [Amount] [Currency]"
    )


def route_message(update, context):
    text = update.message.text
    action = parse_input(text)

    if action["action"] == "recommend_card":
        handle_recommend_card(update, action["shop"], action["amount"], action["currency"])
    elif action["action"] == "show_limits":
        handle_show_limits(update, action["card"])
    elif action["action"] == "add_location":
        handle_add_location(update, action["shop"], action["mcc"])
    elif action["action"] == "delete_location":
        handle_delete_location(update, action["shop"])
    else:
        handle_unknown(update)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    route_message(update, context)


def handle_recommend_card(update, shop: str, amount: float, currency: str):
    dummy_mcc = "5411"

    best_card = None
    best_reward = 0

    for card in CARDS:
        reward = card.calculate_reward(dummy_mcc, currency, amount)
        if reward > best_reward:
            best_reward = reward
            best_card = card

    if best_card:
        update.message.reply_text(
            f"Best card for {shop} at ${amount} is {best_card.get_name()} ({int(best_reward)} miles)"
        )
    else:
        update.message.reply_text(f"No cards available for {shop}")


def handle_show_limits(update, card):
    update.message.reply_text(f"Card: {card}")


def handle_add_location(update, shop, mcc):
    update.message.reply_text(f"Added {shop} with MCC {mcc}")


def handle_delete_location(update, shop):
    update.message.reply_text(f"Deleted {shop}")


def handle_unknown(update):
    update.message.reply_text("Unknown command. Type /start for help.")


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

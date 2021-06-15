import os
import json
import requests
import logging
from formatter import Formatter as f
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = os.environ['telegramkey']

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Hello, this is a Pokédex bot, type /pokemon <number> to search for your Pokémon or /pokemore <number> to see it's full info, but remember, I'm an old school Pokédex, so just Pokémon 1 to 151.")

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def pokemon(update, context):
    try:
        pokemon = int(update.message.text.split(" ")[1])
        request = requests.get('https://www.canalti.com.br/api/pokemons.json')
        pokedex = request.json()
        poke_input = (pokemon - 1)
        update.message.reply_text(f"\tHere's your Pokémon!\nID Number: {pokedex['pokemon'][poke_input]['id']}\nName: {pokedex['pokemon'][poke_input]['name']}\nType: {f.get_types(poke_input)}\n{f.get_photo(poke_input)}")

    except Exception as e:
        print("Error running Pokédex. Command: " + str(update.message.text) + " | Error: " + str(e))
        update.message.reply_text("Failed, bad trainer...")

def pokemore(update, context):
    try:
        pokemon = int(update.message.text.split(" ")[1])
        request = requests.get('https://www.canalti.com.br/api/pokemons.json')
        pokedex = request.json()
        poke_input = (pokemon - 1)
        update.message.reply_text(f"\tHere's your Pokémon full info!\nID Number: {pokedex['pokemon'][poke_input]['id']}\nName: {pokedex['pokemon'][poke_input]['name']}\nType: {f.get_types(poke_input)}\nWeaknesses: {f.get_weaknesses(poke_input)}\nHeight: {pokedex['pokemon'][poke_input]['height']}\nWeight: {pokedex['pokemon'][poke_input]['weight']}\nPrevious Evolution: {f.get_prev_evolutions(poke_input)}\nNext Evolution: {f.get_next_evolutions(poke_input)}\n{f.get_photo(poke_input)}")

    except Exception as e:
        print("Error running Pokédex. Command: " + str(update.message.text) + " | Error: " + str(e))
        update.message.reply_text("Failed, bad trainer...")

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("pokemon", pokemon))
    dp.add_handler(CommandHandler("pokemore", pokemore))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://vmpiresbot.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
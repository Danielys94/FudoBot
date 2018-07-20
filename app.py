'''
    FudoBot
    lista comandi:
    
help - ok.jpg
cavani - <3
pogba - 30!
milan - brocchi
sola - andré silva
dollarumma - $
crudeli - boa! teng! teng! teng!
switch - modalità molesta on/off
    
'''

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, re, random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('A regazzì, e mo vo buco sto pallone.')
    
def herupu(bot, update):
    reply = 'Nella modalità molesta non è necessario inserire /<comando> per attivare il bot.'
    if molesta:
        update.message.reply_text(reply + '\nModalità molesta ON.')
    else:
        update.message.reply_text(reply + '\nModalità molesta OFF.')

def send_sticker(update, sticker_pack):
    update.message.reply_sticker(random.SystemRandom().choice(sticker_pack))

def cavani(bot, update):
    fudo_cavani = bot.get_sticker_set('FudoCavani').stickers
    send_sticker(update, fudo_cavani)

def pogba(bot, update):
    update.message.reply_text('30!')

def milan(bot, update):
    fudo_milan = bot.get_sticker_set('FudoMilan').stickers
    send_sticker(update, fudo_milan)
    
def sola(bot, update):
    fudo_sola = bot.get_sticker_set('FudoSola').stickers
    send_sticker(update, fudo_sola)

def dollarumma(bot, update):
     fudo_dollarumma = bot.get_sticker_set('FudoDollarumma').stickers
     send_sticker(update, fudo_dollarumma)

def crudeli(bot, update):
    fudo_crudeli = bot.get_sticker_set('FudoCrudeli').stickers
    send_sticker(update, fudo_crudeli)

def scan(bot, update):
    global keywords
    for i, v in enumerate(keywords):
        match = re.search(r'\b{}\b'.format(v), update.message.text, flags=re.IGNORECASE)
        if match:
            if i == 0:
                pogba(bot, update)
            elif 1 <= i <= 2:
                milan(bot, update)
            elif i == 3:
                sola(bot, update)
            elif 4 <= i <= 5:
                dollarumma(bot,update)
            elif i == 6:
                crudeli(bot, update)
            else:
                cavani(bot, update)

def switch(bot, update):
    global dp
    global molesta
    global scanhandler
    if molesta:
        molesta = False
        dp.remove_handler(scanhandler)
        update.message.reply_text('Modalità molesta OFF.')
    else:
        molesta = True
        dp.add_handler(scanhandler)
        update.message.reply_text('Modalità molesta ON.')

def error(bot, update, error):
    # Log Errors caused by Updates.
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("664394810:AAEQ1dVh2UoHdDtBz3aHplTrKIRDyPgBuuA")

    # Get the dispatcher to register handlers
    global dp
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', herupu))
    dp.add_handler(CommandHandler('pogba', pogba))
    dp.add_handler(CommandHandler('milan', milan))
    dp.add_handler(CommandHandler('sola', sola))
    dp.add_handler(CommandHandler('dollarumma', dollarumma))
    dp.add_handler(CommandHandler('crudeli', crudeli))
    dp.add_handler(CommandHandler('cavani', cavani))
    global keywords
    keywords = ['pogba','milan','milanista','sola','dollarumma','donnarumma','crudeli','cavani']
    global molesta
    molesta = True
    global scanhandler
    scanhandler = MessageHandler(Filters.text, scan)
    dp.add_handler(scanhandler)
    dp.add_handler(CommandHandler("switch", switch))
    
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()

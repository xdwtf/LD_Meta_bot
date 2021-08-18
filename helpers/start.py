import telegram
import telebot
import logging
import time

# CONFIG

from config import Config

BOT_TOKEN = Config.BOT_TOKEN
LD_DOMAIN = Config.LD_DOMAIN
SECRET = Config.SECRET
ADMIN_IDS = Config.ADMIN_IDS
PIC = Config.PIC
HEROKU_API_KEY = Config.HEROKU_API_KEY
HEROKU_APP_NAME = Config.HEROKU_APP_NAME

try:
    ADMIN_LIST = ADMIN_IDS 
    restricted_mode = True
except:
    ADMIN_LIST = []  # ==> Do Not Touch This !!
    restricted_mode = False

bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

def startmessage(m, botStartTime):
    uptime = get_readable_time((time.time() - botStartTime))
    start_string = "Hoi!!\n\n*I'm Alive Since : *`" + uptime + "`\n\n*For More Info /help*"
    if len(PIC.replace(" ", "")) != 0:
        bot.send_photo(m.chat.id, PIC, caption = start_string, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        bot.send_message(m.chat.id, start_string, parse_mode=telegram.ParseMode.MARKDOWN)

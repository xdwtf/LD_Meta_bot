import telegram
import telebot
import logging
import time

# CONFIG

from config import Config

BOT_TOKEN = Config.BOT_TOKEN
ADMIN_IDS = Config.ADMIN_IDS

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
    start_string = "Hi I'm Alive Since: " + uptime + "xd"
    bot.send_message(m.chat.id, start_string, parse_mode=telegram.ParseMode.MARKDOWN)

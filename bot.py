# -*- coding: utf-8 -*-

import telegram
import telebot
import logging
import requests
import os
import json
import time
import signal
import heroku3
import sys
from telegraph import Telegraph
from functools import wraps
from random import *

# HELPERS / MODULES ==> Didn't Change the folder to modules cause Deploys will be bricked..

from helpers.start import startmessage
from helpers.herokuctrl import hdyno_mod, hrestart_mod, hdynox_mod, hrestartx_mod
from helpers.signal import SIG

# UPTIME

botStartTime = time.time()

# CONFIG

from config import Config

BOT_TOKEN = Config.BOT_TOKEN
ADMIN_IDS = Config.ADMIN_IDS
HEROKU_API_KEY = Config.HEROKU_API_KEY
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEYX = Config.HEROKU_API_KEYX
HEROKU_APP_NAMEX = Config.HEROKU_APP_NAMEX
BOT_USERNAME = Config.BOT_USERNAME

# ADMIN / OWNER

try:
    ADMIN_LIST = ADMIN_IDS
    if len(ADMIN_LIST) != 0:
        restricted_mode = True
    else:
        restricted_mode = False
except:
    ADMIN_LIST = []  # ==> Do Not Touch This !!
    restricted_mode = False

# BOT CODE

bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

CHAT_IDS = ADMIN_IDS.split()

for i in CHAT_IDS:
    if len(i) != 0 and i.isnumeric() == True:
        bot.send_message(int(i), "`Hey ! The Bot Is Up and Running !`", parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        pass

allchar = "abcdefghijklmnopqrstuvwxyz0123456789"

def restricted(func):
    @wraps(func)
    def wrapped(update, *args, **kwargs):
        chat_id = update.chat.id
        user_id = update.from_user.id
        if str(chat_id).startswith("-100"):
            if (grprestricted_mode) and (str(chat_id) not in GRP_LIST):
                print("Unauthorized access denied for {}.".format(chat_id))
                bot.send_message(update.chat.id, "*Error :\t\t*This Group is not Authorized to access the bot.\n\nPls Add Chat ID to Config Vars.\n\n[Contact Bot Developer](https://t.me/shrey_contact_bot) !!", parse_mode='Markdown', disable_web_page_preview=True)
                return
            elif update.text.split("@"+BOT_USERNAME)[0][1:] not in GROUP_COMMANDS:
                bot.send_message(update.chat.id, "*Error :\t\t*This Command can only be used by *Bot Admin* and in *Private Only* !!", parse_mode='Markdown', disable_web_page_preview=True)
                return
            elif "help" in update.text:
                grphelp(m=update)
                return
        else:
            if (restricted_mode) and (str(chat_id) not in ADMIN_LIST):
                print("Unauthorized access denied for {} - {}.".format(user_id, update.from_user.username))
                bot.send_message(update.chat.id, "*Error :\t\t*You are not Authorized to access the bot.\n\nPls Add Chat ID to Config Vars.\n\n[Contact Bot Developer](https://t.me/shrey_contact_bot) !!", parse_mode='Markdown', disable_web_page_preview=True)
                return
        return func(update, *args, **kwargs)
    return wrapped

@bot.message_handler(commands=['start','hi'])
@restricted
def start(m):
    startmessage(m, botStartTime)

@bot.message_handler(commands=['hrestart'])
def hrestart(m):
    hrestart_mod(m)

@bot.message_handler(commands=['hdyno'])
def hdyno(m):
    hdyno_mod(m)

@bot.message_handler(commands=['hrestartx'])
def hrestartx(m):
    hrestartx_mod(m)

@bot.message_handler(commands=['hdynox'])
def hdynox(m):
    hdynox_mod(m)

signal.signal(signal.SIGINT, SIG.sigint_handler)
signal.signal(signal.SIGTERM, SIG.sigterm_handler)

bot.polling(none_stop=True, timeout=999999)

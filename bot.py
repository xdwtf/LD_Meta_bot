# -*- coding: utf-8 -*-

import telegram
import telebot
import logging
import requests
import os
import json
import time
import heroku3
from telegraph import Telegraph
from functools import wraps
from random import *

# HELPERS / MODULES ==> Didn't Change the folder to modules cause Deploys will be bricked..

from helpers.start import startmessage
from helpers.speedtest import speedtestmes
from helpers.rebuild import rebuildmes
from helpers.restart import restartmes
from helpers.search import searchmes
from helpers.find import findmes
from helpers.herokuctrl import hdyno_mod, hrestart_mod
from helpers.m3u8 import getm3u8
from helpers.help import helpmes, help_update_message, grphelp, help_update_keyboard
from helpers.config import configmes, config_update_message, config_update_keyboard
from helpers.categories import  catsetup, cat_update_message, cat_update_keyboard, action_category, action_keyboard, action_listcategory, action_addcategory
from helpers.bot_id import configsetups
from helpers.accounts import accountsetup
from helpers.settings import settingsedit

# UPTIME

botStartTime = time.time()

# CONFIG

from config import Config

BOT_TOKEN = Config.BOT_TOKEN
LD_DOMAIN = Config.LD_DOMAIN
SECRET = Config.SECRET
ADMIN_IDS = Config.ADMIN_IDS
GROUP_IDS = Config.GROUP_IDS
PIC = Config.PIC
HEROKU_API_KEY = Config.HEROKU_API_KEY
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
BOT_USERNAME = Config.BOT_USERNAME

# ADMIN / OWNER

try:
    ADMIN_LIST = ADMIN_IDS 
    restricted_mode = True
except:
    ADMIN_LIST = []  # ==> Do Not Touch This !!
    restricted_mode = False

ADMIN_CMD = [
    'restart',
    'fixconfig',
    'assignid',
    'unassignid',
    'accounts',
    'accountsclip', 
    'addaccount', 
    'rmaccount',
    'rmaccid', 
    'categories', 
    'setanilist', 
    'addcategory', 
    'rmcategory', 
    'settings', 
    'config', 
    'set', 
    'ui', 
    'setui',
    'hdyno',
    'hrestart',
    'speedtest'
]

# GROUPS

try:
    GRP_LIST = GROUP_IDS
    grprestricted_mode = True
except:
    GRP_LIST = []  # ==> Do Not Touch This !!
    grprestricted_mode = True

bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

CHAT_IDS = ADMIN_IDS.split()

# BOT CODE

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
                print("Unauthorized access denied for {}.".format(user_id))
                bot.send_message(update.chat.id, "*Error :\t\t*This Group is not Authorized to access the bot.\n\nPls Add Chat ID to Config Vars.\n\n[Contact Bot Developer](https://t.me/shrey_contact_bot) !!", parse_mode='Markdown', disable_web_page_preview=True)
                return
            elif any(cmd == update.text.split("@"+BOT_USERNAME)[0][1:] for cmd in ADMIN_CMD):
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

@bot.message_handler(commands=['help'])
@restricted
def help(m):
    helpmes(m)

@bot.message_handler(commands=['grouphelp'])
@restricted
def grouphelp(m):
    grphelp(m)

@bot.message_handler(commands=['speedtest'])
@restricted
def speedtest(m):
    speedtestmes(m)    

@bot.message_handler(commands=['rebuild'])
@restricted
def rebuild(m):
    rebuildmes(m)

@bot.message_handler(commands=['restart'])
@restricted
def restart(m):
    restartmes(m)

@bot.message_handler(commands=['fixconfig'])
@restricted
def fixconfig(m):
    configsetups.fixconfigmes(m)

@bot.message_handler(commands=['assignid'])
@restricted
def assignid(m):
    configsetups.assignidmes(m)

@bot.message_handler(commands=['unassignid'])
@restricted
def unassignid(m):
    configsetups.unassignidmes(m)

@bot.message_handler(commands=['accounts'])
@restricted
def accounts(m):
    accountsetup.accountsmes(m)

@bot.message_handler(commands=['accountsclip'])
def accountsclip(m):
    accountsetup.accountsclipmes(m)

@bot.message_handler(commands=['addaccount'])
@restricted
def addaccount(m):
    accountsetup.addaccountmes(m)

@bot.message_handler(commands=['rmaccount'])
@restricted
def rmaccount(m):
    accountsetup.rmaccountmes(m)

@bot.message_handler(commands=['rmaccid'])
@restricted
def rmaccid(m):
    accountsetup.rmaccidmes(m)

@bot.message_handler(commands=['categories'])
@restricted
def categories(m):
    catsetup.categories_mod(m)

@bot.message_handler(commands=['setanilist'])
@restricted
def setanilist(m):
    catsetup.setanilist_mod(m)

@bot.message_handler(commands=['addcategory'])
@restricted
def addcategory(m):
    catsetup.addcategory_mod(m)

@bot.message_handler(commands=['rmcategory'])
@restricted
def rmcategory(m):
    catsetup.rmcategory_mod(m)

@bot.message_handler(commands=['config'])
@restricted
def config(m):
    configmes(m)

@bot.message_handler(commands=['settings'])
@restricted
def settings(m):
    settingsedit.settings_mod(m)

@bot.message_handler(commands=['set'])
@restricted
def set(m):
    settingsedit.set_mod(m)

@bot.message_handler(commands=['ui'])
@restricted
def ui(m):
    settingsedit.ui_mod(m)

@bot.message_handler(commands=['setui'])
@restricted
def setui(m):
    settingsedit.setui_mod(m)

@bot.message_handler(commands=['hrestart'])
def hrestart(m):
    hrestart_mod(m)

@bot.message_handler(commands=['hdyno'])
def hdyno(m):
    hdyno_mod(m)

@bot.message_handler(commands=['search'])
@restricted
def search(m):
    searchmes(m)

@bot.message_handler(commands=['find'])
@restricted
def find(m):
    findmes(m)

@bot.message_handler(commands=['m3u8'])
@restricted
def m3u8(m):
    getm3u8(m)

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global data
    data = query.data
    get_callback(query)

def get_callback(query):
    bot.answer_callback_query(query.id)
    if data == 'instructions' or data == 'help' or data == 'closehelp':
        help_update_message(query.message, data)
    elif data == '1' or data == '2' or data == '3' or data == 'close':
        config_update_message(query.message, data)
    elif data == 'movies' or data == 'tv_shows' or data == 'amovies' or data == 'atv_shows':
        cat_update_message(query.message, data)
        action_addcategory(query.message, data)
    else:
        cat_update_message(query.message, data)
        action_keyboard(query.message, data)
            
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global data
    data = query.data
    get_callback(query)

bot.polling(none_stop=True, timeout=999999)

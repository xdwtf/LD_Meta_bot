import telegram
import telebot
import logging
import requests
from telegraph import Telegraph
from helpers.groupcmd import grpcmd

# CONFIG

from config import Config

BOT_TOKEN = Config.BOT_TOKEN
LD_DOMAIN = Config.LD_DOMAIN
LDX_DOMAIN = Config.LDX_DOMAIN
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

def findmes(m):
    chat = grpcmd(m, "find")
    if chat == "":
        bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
        \n*To Search for Content :-*
        Send /find `<search_query>`
        """, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        query = grpcmd(m, "find")
        try:
            telegraph = Telegraph()

            telegraph_acc = telegraph.create_account(
                short_name="WeebFlix",
                author_name="WeebFlix",
                author_url="https://telegram.dog/weebflix"
            )

            search_results = bot.send_message(m.chat.id, "`Searching Your Request...`\n\n`Query` : *{}*".format(query), parse_mode=telegram.ParseMode.MARKDOWN)

            url_conf = "https://{}/api/v1/config?secret={}".format(LD_DOMAIN, SECRET)

            r1 = requests.get(url_conf)
            res1 = r1.json()
            search_acc_auth = res1["content"]["account_list"][0]["auth"]

            url_meta = "https://{}/api/v1/metadata?a={}&q={}".format(LD_DOMAIN, search_acc_auth, query)

            r2 = requests.get(url_meta)
            res2 = r2.json()

            html_string = ""
            num_of_results = 0

            if res2["code"] == 200 and res2["success"] == True:
                for cat in res2["content"]:
                    if len(cat["children"]) == 0:
                        continue
                    for media in cat["children"]:
                        num_of_results += 1
                        title = media["title"]
                        type_ = cat["categoryInfo"]["type"]
                        releaseDate = media["releaseDate"] if "releaseDate" in media.keys() else ""
                        backdrop = media["backdropPath"] if "backdropPath" in media.keys() else ""
                        overview = media["overview"] if "overview" in media.keys() else ""
                        if str(type_) == "TV Shows":
                            url_show = "https://{}/view/{}".format(LDX_DOMAIN, media["id"])
                            f_html = "<b> - View Link : </b> <a href='{}'>Click Here To Watch !</a> <br>".format(url_show)

                        else:
                            url_mov = "https://{}/view/{}".format(LDX_DOMAIN, media["id"])
                            f_html = "<b> - View Link : </b><a href={}>Click Here To Watch !</a> !!<br>".format(url_mov)

                        TG_html = '''<p>
                                            <img src=''' + str(backdrop) + '''>
                                            <b>Name : </b><code>''' + str(title) + '''</code><br>
                                            <b> - Overview : </b><code>''' + str(overview) + '''</code><br>
                                            <b> - Release Date : </b><code>''' + str(releaseDate) + '''</code><br>
                                            <b> - Type : </b><code>''' + str(type_) + '''</code><br>
                                            {}<br>➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖<br>
                                        </p>'''.format(f_html)

                        html_string += TG_html
            if num_of_results != 0:
                telegraph_res = telegraph.create_page(
                    title="WeebFlix Search Results",
                    html_content=html_string,
                    author_name='WeebFlix',
                    author_url='https://telegram.dog/weebflix'
                )

                telegraph_url = 'https://telegra.ph/{}'.format(telegraph_res['path'])
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.row(
                    telebot.types.InlineKeyboardButton("🔍 Search Results", url=telegraph_url)
                )
                bot.edit_message_text("`Query` : *{}*\n\n`Found `*{}*` Matching Search Results !!`".format(query, str(num_of_results)), m.chat.id, message_id=search_results.message_id, reply_markup=keyboard, parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.edit_message_text("*No Matching Search Results !!*", m.chat.id, message_id=search_results.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.edit_message_text("`Server Not Accessible !!`", m.chat.id, message_id=search_results.message_id, parse_mode=telegram.ParseMode.MARKDOWN)

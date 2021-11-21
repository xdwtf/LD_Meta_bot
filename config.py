import os

# CLASSES
class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    ADMIN_IDS = os.environ.get("ADMIN_IDS", "")
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", "")
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", "")
    HEROKU_API_KEYX = os.environ.get("HEROKU_API_KEYX", "")
    HEROKU_APP_NAMEX = os.environ.get("HEROKU_APP_NAMEX", "")
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "")

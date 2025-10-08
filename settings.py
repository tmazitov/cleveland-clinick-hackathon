import logging
import dotenv
import os

# Telegram Bot API Key
BOT_API_KEY = dotenv.get_key(dotenv_path='.env', key_to_get='BOT_API_KEY')

# OpenAI API Key
OPENAI_API_KEY = dotenv.get_key(dotenv_path='.env', key_to_get='OPENAI_API_KEY')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Absolute path to root folder
DIR = os.path.abspath(os.path.dirname(__file__))
MEDIA = f"{DIR}/media"
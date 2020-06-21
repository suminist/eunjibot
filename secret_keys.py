import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
LF_API_KEY = os.getenv('LF_API_KEY')
LF_API_SECRET = os.getenv('LF_API_SECRET')
MONGODB_CONNECTION = os.getenv('MONGODB_CONNECTION')

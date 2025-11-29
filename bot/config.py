from dotenv import load_dotenv
from os import getenv

load_dotenv()

SUPABASE_URL = getenv('SUPABASE_URL')
SUPABASE_KEY = getenv('SUPABASE_KEY')
SUPABASE_API_SCHEMA = getenv('SUPABASE_API_SCHEMA')

TOKEN = getenv('TOKEN')
GIF = getenv('GIF')
WOMEN = getenv('WOMEN')

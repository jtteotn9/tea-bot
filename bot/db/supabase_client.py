import logging
import sys
from supabase import create_client, Client
from ..config import SUPABASE_KEY, SUPABASE_URL


try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logging.info(f"Инициализация прошла успешно")
except Exception as e:
    logging.error(f"Ошибка инициализации Supabase: {e}")
    sys.exit(1)
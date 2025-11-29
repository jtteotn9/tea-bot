import logging
import sys
from typing import Optional

from supabase import Client, create_client

from ..config import SUPABASE_KEY, SUPABASE_URL, SUPABASE_API_SCHEMA


class SupabaseClient:
    def __init__(self, url: str, key: str, schema: Optional[str]=None):
        self.client: Client = create_client(url, key)
        self.schema_name = schema or 'public'

    @property
    def schema(self):
        return self.client.schema(self.schema_name)

    @property
    def users(self):
        return self.schema.table('users')

    @property
    def tea_log(self):
        return self.schema.table('tea_log')

    @property
    def storage(self):
        return self.client.storage

try:
    supabase =  SupabaseClient(SUPABASE_URL, SUPABASE_KEY, SUPABASE_API_SCHEMA)
    logging.info(f"Инициализация прошла успешно")
except Exception as e:
    logging.error(f"Ошибка инициализации Supabase: {e}")
    sys.exit(1)

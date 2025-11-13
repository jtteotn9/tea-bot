import logging
from .supabase_client import supabase
from typing import Dict, Any, List

def get_user(user_id: int):
    """Returns user_id if exists"""
    try:
        response = supabase.table('users').select('name').eq('user_id', user_id).execute()
        if response.data:
            return response.data[0]
    except Exception as e:
        logging.error(f"Ошибка получения пользователя {user_id}: {e}")
    return None

def add_user(user_data: Dict[str, Any]):
    """Add user"""
    try:
        supabase.table('users').insert(user_data).execute()
        return True
    except Exception as e:
        logging.error(f"Ошибка добавления пользователя {user_data.get('user_id')}: {e}")
        return False

def add_tea_log(tea_data: Dict[str, Any]):
    """Add tea log"""
    try:
        supabase.table('tea_log').insert(tea_data).execute()
        return True
    except Exception as e:
        logging.error(f"Ошибка добавления чая {tea_data.get('user_id')}: {e}")
        return False

def get_user_teas(user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
    """Returns {limit} tea logs"""
    try:
        response = supabase.table("tea_log") \
                           .select("name, tea_type, rating, photo_url, price, purchase_location") \
                           .eq("user_id", user_id) \
                           .order("created_at", desc=True) \
                           .limit(limit) \
                           .execute()
        return response.data
    except Exception as e:
        logging.error(f"Ошибка получения чаев {user_id}: {e}")
        return []

def upload_tea_photo(file_name: str, file_content: bytes) -> str:
    """Returns photo's url from Supabase"""
    try:
        supabase.storage.from_("tea").upload(
            path=file_name,
            file=file_content,
            file_options={"content-type": "image/jpeg", "upsert": "true"}
        )
        public_url = supabase.storage.from_("tea").get_public_url(file_name)
        return public_url
    except Exception as e:
        logging.error(f"Ошибка загрузки фото в Storage: {e}")
        return None

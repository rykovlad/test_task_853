import json
import os

from telethon.sync import TelegramClient


def create_client(session_name: str):
    """
        Creates a Telethon client using session data from a json file

        :param session_name:
        :param proxy: Проксі (type, host, port, username, password)
        :param session: Шлях до сесії

        :return: TelegramClient
    """
    session_number = os.getenv('SESSION_NUMBER')
    json_file = f"tg_sessions/{session_name}.json"
    session_file = f"tg_sessions/{session_name}.session"
    with open(json_file, "r") as file:
        account = json.load(file)
    proxy = account.get('proxy')
    return TelegramClient(
        session_file, api_id=account.get("app_id") or account.get("api_id"),
        api_hash=account.get("app_hash") or account.get("api_hash"),
        system_version=account.get("sdk"),
        app_version=account["app_version"],
        device_model=account.get("device") or account.get("device_model"),
        proxy=(proxy[0], proxy[1], int(proxy[2]),
               True, proxy[4], proxy[5]) if proxy else None)

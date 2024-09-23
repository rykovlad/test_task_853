import requests

from group_parser import GroupParser
from create_client import create_client
from parser.tmodels import User, Group

URL = 'http://localhost:8000/'

def push_to_api(chat: Group, users: list[User]):
    for user in users:
        response = requests.post(URL + "users/", json=user.to_json())

        if response.status_code == 200:
            print('Користувача створено успішно')
            print('Відповідь сервера:', response.json())
        else:
            print('Помилка при створенні користувача')
            print('Код статусу:', response.status_code)
            print('Текст відповіді:', response.json())

    response = requests.post(URL + "groups/", json=chat.to_json())
    if response.status_code == 200:
        print('групу створено успішно')
        print('Відповідь сервера:', response.json())
    else:
        print('Помилка при створенні групи')
        print('Код статусу:', response.status_code)
        print('Текст відповіді:', response.json())


TARGET_CHAT_USERNAME = "dubaipara"

# session_numb = "13464970232"


def parse_and_push(target_chat_username, session_numb):
    client = create_client(session_numb)
    target_chat, users_list = GroupParser(target_chat_username, client).run()
    push_to_api(target_chat, users_list)

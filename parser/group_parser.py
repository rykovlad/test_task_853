
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from loguru import logger


from tmodels import User, Group



class GroupParser:
    def __init__(self, username, client):
        self.username = username
        self.client = client

    async def __group_parser(self):
        chat = await self.client(ResolveUsernameRequest(self.username))
        full_chat = await self.client(GetFullChannelRequest(chat))
        participants_count = full_chat.full_chat.participants_count

        target_chat = Group(chat.chats[0].id, chat.chats[0].title,
                            chat.chats[0].username)

        # get users from participants list
        users_list, tid_list = await self.__parse_by_participants(chat)

        # additionally get users by parsing msgs
        if participants_count > 10_000:
            users_list_2nd_part, tid_list_2nd_part = await self \
                .__parse_by_msgs(chat, tid_list)
            users_list.extend(users_list_2nd_part)
            tid_list.extend(tid_list_2nd_part)

        target_chat.add_users(tid_list)
        return target_chat, users_list

    async def __parse_by_participants(self, chat):
        users_list = []
        tid_list = []
        async for user in self.client.iter_participants(chat):
            if not user.bot:
                users_list.append(User(user.id, user.first_name,
                                       user.last_name, user.username))
                tid_list.append(user.id)
                logger.info(f"1st way, {user.id}")

        return users_list, tid_list

    async def __parse_by_msgs(self, chat, tid_list):
        users_list = []
        async for x in self.client.iter_messages(chat):
            try:
                if not x.sender.bot \
                        and (x.sender.id not in tid_list) \
                        and x.sender.first_name:
                    tid_list.append(x.sender.id)
                    users_list.append(User(x.sender.id,
                                           x.sender.first_name,
                                           x.sender.last_name,
                                           x.sender.username))
                    logger.info(f"2nd way, {x.sender.id}")
            except AttributeError:
                pass
        return users_list, tid_list

    def run(self):
        with self.client:
            target_chat, users_list = self.client.loop. \
                run_until_complete(self.__group_parser())

        return target_chat, users_list


'''
# exemple to activate

_client = create_client("13465417178")
TARGET_CHAT_USERNAME = "dubaipara"
target_chat, users_list = GroupParser(TARGET_CHAT_USERNAME, _client).run()

with open("notbase.txt", "a", encoding="utf-8") as f:
    f.write(str(target_chat))
    for u in users_list:
        f.write(str(u))
'''

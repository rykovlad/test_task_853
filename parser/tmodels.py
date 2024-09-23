

class BaseObject:
    def __init__(self, tid: int, username: str | None = None):
        self.tid = tid
        self.username = username


class User(BaseObject):
    def __init__(self, tid: int, first_name: str,
                 last_name: str | None = None, username: str | None = None):
        super().__init__(tid, username=username)
        self.first_name = first_name
        self.last_name = last_name
        self.groups = None

    def add_users(self, groups: list[int]):
        self.groups = groups

    def __str__(self):
        return (f'{str(self.tid)} - {self.first_name} '
                f'{self.last_name if self.last_name else ""} '
                f'{self.username if self.username else ""}\n')

    def to_json(self):
        return {
            'tid': self.tid,
            'first_name': self.first_name,
            'last_name': self.last_name if self.last_name else None,
            'username': self.username if self.username else None,
            'groups': self.groups if self.groups else []
        }


class Group(BaseObject):
    def __init__(self, tid: int, name: str, username: str | None = None):
        super().__init__(tid, username=username)
        self.name = name
        self.users = None

    def add_users(self, users: list[int]):
        self.users = users

    def __str__(self):
        return (f'{str(self.tid)} - {self.name} '
                f'{self.username if self.username else ""}\n')

    def to_json(self):
        return {
            'tid': self.tid,
            'name': self.name,
            'username': self.username if self.username else None,
            'users': self.users if self.users else []
        }
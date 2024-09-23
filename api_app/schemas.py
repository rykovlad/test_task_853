from pydantic import BaseModel


class User(BaseModel):
    tid: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    groups: list[int] | int | None = None


class PatchUser(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    groups: list[int] | int | None = None


class Group(BaseModel):
    tid: int
    name: str
    username: str | None = None
    users: list[int] | int | None = None


class PatchGroup(BaseModel):
    name: str | None = None
    username: str | None = None
    users: list[int] | int | None = None

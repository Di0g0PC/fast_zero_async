from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class Userschema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(Userschema):
    id: int


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserList(BaseModel):
    users: list[UserPublic]

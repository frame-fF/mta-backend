from ninja import Schema
from typing import Optional
from ninja import ModelSchema
from apps.player.models import Player

class RegisterSchema(Schema):
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class LoginSchema(Schema):
    username: str
    password: str


class PlayerSchema(ModelSchema):

    class Meta:
        model = Player
        fields = ["id", "username", "email", "first_name", "last_name"]
    


class MessageSchema(Schema):
    message: str


class TokenSchema(Schema):
    token: str
    user: PlayerSchema

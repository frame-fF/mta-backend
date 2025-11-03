from django.urls import path
from apps.player.api import *

app_name = "player_api"

urlpatterns = [
    path("login/", LoginAPI.as_view(), name="login"),
    path("register/", RegisterAPI.as_view(), name="register"),
    path("me/", PlayerAPI.as_view(), name="player"),
    path("me/data/update/", UpdatePlayerDataAPI.as_view(), name="update_player_data"),
]

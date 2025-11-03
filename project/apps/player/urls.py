from django.urls import path
from ninja import NinjaAPI
from apps.player.api import router as player_router

api = NinjaAPI()

# Register routers
api.add_router("/player/", player_router)

urlpatterns = [
    path("", api.urls),
]

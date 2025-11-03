from rest_framework import serializers
from rest_framework.authtoken.models import Token
from apps.player.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"


class TokenSerializer(serializers.ModelSerializer):
    user = PlayerSerializer()

    class Meta:
        model = Token
        fields = "__all__"

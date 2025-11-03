from rest_framework import serializers
from rest_framework.authtoken.models import Token
from apps.player.models import Player, PlayerData

class PlayerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerData
        fields = "__all__"


class PlayerSerializer(serializers.ModelSerializer):
    data = PlayerDataSerializer()
    class Meta:
        model = Player
        fields = "__all__"


class TokenSerializer(serializers.ModelSerializer):
    user = PlayerSerializer()

    class Meta:
        model = Token
        fields = "__all__"

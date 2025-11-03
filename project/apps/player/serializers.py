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


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, label='Confirm Password', style={'input_type': 'password'})

    class Meta:
        model = Player
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = Player.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Create PlayerData for the new user
        PlayerData.objects.create(player=user)
        return user

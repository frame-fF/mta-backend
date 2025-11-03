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
    email = serializers.EmailField(required=True)

    class Meta:
        model = Player
        fields = ['username', 'email', 'password', 'password2']

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        if Player.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if Player.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

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

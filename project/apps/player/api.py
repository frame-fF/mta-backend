from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status
from apps.player.serializers import TokenSerializer, RegisterSerializer, PlayerSerializer
from apps.player.models import Player
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class LoginAPI(APIView):
    def get(self, request, *args, **kwargs):
        # Return serializer schema for browsable API
        serializer = AuthTokenSerializer()
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        Token.objects.filter(user=user).delete()  # Ensure old tokens are deleted
        token = Token.objects.create(user=user)
        serializer = TokenSerializer(instance=token)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterAPI(APIView):
    def get(self, request, *args, **kwargs):
        # Return serializer schema for browsable API
        serializer = RegisterSerializer()
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create token for the new user
            token = Token.objects.create(user=user)
            token_serializer = TokenSerializer(instance=token)
            return Response(token_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetPlayerAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = PlayerSerializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
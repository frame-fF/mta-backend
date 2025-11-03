from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status
from apps.player.serializers import TokenSerializer


class LoginAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        Token.objects.filter(user=user).delete()  # Ensure old tokens are deleted
        token = Token.objects.create(user=user)
        serializer = TokenSerializer(instance=token)
        return Response(serializer.data, status=status.HTTP_200_OK)

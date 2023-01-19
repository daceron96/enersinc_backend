from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.person.api.serializers import CustomTokenObtainPairSerializer, UserSerializer

class LoginView(TokenObtainPairView):
  serializer_class = CustomTokenObtainPairSerializer

  def post(self, request, *args, **kwargs):
    username = request.data.get("username","")
    password = request.data.get("password","")
    user = authenticate(
      username = username,
      password = password
    )

    if user:
      login_serializer = self.serializer_class(data = request.data)
      if login_serializer.is_valid():
        user_serializer = UserSerializer(user)
        return Response({
          'token' : login_serializer.validated_data.get("access"),
          'refresh-token': login_serializer.validated_data.get('refresh'),
          'user' : user_serializer.data,
          'message' : "Inicion de sesion exitoso"
        }, status = status.HTTP_200_OK)
      return Response({
        'error': 'Contraseña o nombre de usuario incorrectos'
        }, status=status.HTTP_400_BAD_REQUEST)
    return Response({
      'error': 'Contraseña o nombre de usuario incorrectos'
      }, status=status.HTTP_400_BAD_REQUEST)

class ValidateTokenView(APIView):
  authentication_classes = (JWTAuthentication,)

  def get(self, request):
    user = request.user
    user_serializer = UserSerializer(user)
    return Response(user_serializer.data, status=status.HTTP_200_OK) 


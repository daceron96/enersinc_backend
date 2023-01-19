from rest_framework import serializers
from apps.person.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class PersonSerializer(serializers.ModelSerializer):
  
  password2 = serializers.CharField(max_length = 100, write_only=True)

  class Meta:
    model = User
    exclude = ("is_active","is_staff","is_superuser")
    extra_kwargs = {'password': {'write_only': True}}
  
  def validate(self, data):
    if(data["password"] != data["password2"]):
      raise serializers.ValidationError({
        "password" :"Las contraseñas ingresadas no coinciden",
        "password2" :"Las contraseñas ingresadas no coinciden",
    })
    return data

  def create(self, validated_data):
    validated_data.pop("password2")
    user = User(**validated_data)
    user.set_password(validated_data['password'])
    user.save()
    return user

class PersonUpdateSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    exclude = ("is_active","is_staff","is_superuser", "password")

class PersonListSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ("email","lastName","name", "username", "id")

class PersonRetrieveSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ("email","lastName","name", "username", "id", "hobbie", "documentNumber", "phone", "documentType")

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
  pass
  
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ("username", "name", "lastName")
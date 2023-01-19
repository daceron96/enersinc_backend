from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
  def _create_user(self, username, email, name,lastName, password, is_staff, is_superuser, **extra_fields):
    user = self.model(
      username = username,
      email = email,
      name = name,
      lastName = lastName,
      is_staff = is_staff,
      is_superuser = is_superuser,
      **extra_fields
    )
    user.set_password(password)
    user.save(using=self.db)
    return user

  def create_user(self, username, email, name,lastName, password=None, **extra_fields):
   return self._create_user(username, email, name,lastName, password, False, False, **extra_fields)

  def create_superuser(self, username, email, name,lastName, password=None, **extra_fields):
   return self._create_user(username, email, name,lastName, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

  DOCUMENT_TYPE_CHOICES = [
    ("CC" , "CEDULA DE CIUDADANIA"),
    ("CE" , "CEDULA DE EXTRANJERIA"),
    ("NIP" , "NUMERO DE IDENTIFICACION PERSONAL"),
    ("NIT" , "NUMERO DE IDENTIFICACION TRIBUTARIA"),
    ('TI' , "TARJETA DE IDENTIDAD"),
    ("PAP" , "PASAPORTE")

  ]
  
  username = models.CharField(
    max_length= 100, 
    unique=True,
    error_messages={'unique':"Ya existe un usuario con este mismo nombre de usuario."}
    )
  email = models.EmailField(
    max_length=100, 
    unique=True,
    error_messages={'unique':"Ya existe un usuario con este correo."}
    )
  documentType = models.CharField(max_length=3, choices=DOCUMENT_TYPE_CHOICES)
  documentNumber = models.CharField(
    max_length= 20, 
    unique=True,
    error_messages={'unique':"Ya existe un usuario con este numero de identificacion."}
    )
  name = models.CharField(max_length=50)
  lastName = models.CharField(max_length=50)
  hobbie = models.CharField(max_length= 255)
  phone = models.CharField(max_length=100)
  is_active = models.BooleanField(default = True)
  is_staff = models.BooleanField(default = False)
  is_superuser = models.BooleanField(default = False)
  objects = UserManager()

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email','name','lastName']

  class Meta:
    ordering = ["name"]

  def __str__(self) -> str:
    return f'{self.name} {self.lastName}'
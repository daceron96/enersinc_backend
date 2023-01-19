from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import (PersonSerializer, PersonRetrieveSerializer, PersonListSerializer, 
PersonUpdateSerializer)

class PersonViewSet(viewsets.ModelViewSet):
  serializer_class = PersonSerializer
  retrieve_serializer = PersonRetrieveSerializer
  list_serializer = PersonListSerializer
  update_serializer = PersonUpdateSerializer

  def get_queryset(self, pk=None):
    return self.get_serializer().Meta.model.objects.filter(is_active=True)

  def list(self, request):
    queryset = self.get_queryset()
    person_serializer = self.list_serializer(queryset, many = True)
    return Response(person_serializer.data, status= status.HTTP_200_OK)

  def retrieve(self, request, pk = None):
    person = self.get_queryset().get(pk = pk)
    if person:
      person_serializer = self.retrieve_serializer(person)
      return Response(person_serializer.data, status = status.HTTP_200_OK)
    return Response({'error':'No existe un usuario con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

  def create(self, request):
    person_serializer = self.serializer_class(data = request.data)
    if person_serializer.is_valid():
      person_serializer.save()
      return Response({
        'message' : 'Usuario registrado correctamente!!',
        'data' : person_serializer.data
      }, status = status.HTTP_201_CREATED)
    return Response({
      'message' : 'Hay errores en el formulario!!', 
      'errors' :person_serializer.errors}
      , status = status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    person = self.get_queryset().get(pk = pk)
    if(person):
      person_serializer = self.update_serializer(instance = person, data=request.data, partial = True)
      if(person_serializer.is_valid()):
        person_serializer.save()
        return Response({
          "message": "Informacion de usuario actualizado correctamente",
          "data" : self.list_serializer(person_serializer.data).data
          }, status=status.HTTP_200_OK)
      return Response({
        'message':'Hay errores en el formulario!!', 
        'errors':person_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message" : "El usuario no existe"}, status=status.HTTP_404_NOT_FOUND)

  def destroy(self, request, pk=None):
    person = self.get_queryset().get(pk = pk)
    if person:
      person.delete()
      return Response({
        'message' : "Usuario eliminado correctamente"
        }, status = status.HTTP_200_OK)
    return Response({
      'message': 'No existe un usuario registrado con estos datos'
      }, status = status.HTTP_400_BAD_REQUEST)


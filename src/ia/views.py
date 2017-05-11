from django.shortcuts import render
from django.contrib.auth.models import Group
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.db import connection
from django.db import models
from django.db import connections

import json
import datetime

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.utils import translation
# from django_filters.rest_framework import DjangoFilterBackend
# from django_filters import rest_framework as filters

import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from ia.models import Pais, Estado, Ciudad
from ia.models import Usuario, Cia, UserCia, UserLog, Persona, PersonaJuridica, PersonaNatural
from ia.models import Producto, Direccion, SesionTrabajo, DocRep, DocRepDet, CiaConsecutivo

from ia.serializers import GroupSerializer
from ia.serializers import PaisSerializer, EstadoSerializer, CiudadSerializer
from ia.serializers import UsuarioSerializer, CiaSerializer, UserCiaSerializer, UserLogSerializer, PersonaSerializer
from ia.serializers import PersonaJuridicaSerializer, PersonaNaturalSerializer
from ia.serializers import ProductoSerializer, DireccionSerializer, SesionTrabajoSerializer
from ia.serializers import DocRepSerializer, DocRepDetSerializer, CiaConsecutivoSerializer


# Create your views here.

def dictfetchall(cursor):
    # Returns all rows from a cursor as a dict
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


@api_view(['GET'])
def selectraw(request):
    query = """
            SELECT *
            FROM pais, estado 
            WHERE ( pais.pais_id = estado.pais_id ) 
            """
    cursor = connection.cursor()
    cursor.execute(query)
    return HttpResponse(json.dumps(dictfetchall(cursor)), content_type="application/json; charset=utf-8")


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profiles."""

    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class EstadoFilter(django_filters.rest_framework.FilterSet):
    edo_ini = django_filters.NumberFilter(name="estado_id", lookup_expr='gte')
    edo_fin = django_filters.NumberFilter(name="estado_id", lookup_expr='lte')
    nombrelike = django_filters.CharFilter(name="nombre", lookup_expr='icontains')
    class Meta:
        model = Estado
        fields = ['pais', 'nombrelike', 'edo_ini', 'edo_fin' ]            

class EstadoViewSet(viewsets.ModelViewSet):
    """ 
    Estados 
    """
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = EstadoFilter
    ordering_fields = ('nombre', )

    def create(self, request):
        request.session[settings.LANGUAGE_SESSION_KEY] = 'es-VE'
        pais_id = int(request.data['pais'])
        pais = Pais.objects.get(pk=pais_id)
        estado = Estado.objects.create(
            nombre=request.data['nombre'],
            codigo=request.data['codigo'],
            pais=pais
        )

        serializer = EstadoSerializer(instance=estado)
        return Response(serializer.data)

    def update(self, request, pk):
        # estado_id = int(request.data['estado_id'])
        pais_id = int(request.data['pais_id'])
        nombre=request.data['nombre']
        codigo=request.data['codigo']
        pais = Pais.objects.get(pk=pais_id)
        estado = Estado.objects.get(pk=pk)
        estado.pais=pais
        estado.nombre=nombre
        estado.codigo=codigo
        estado.save()

        serializer = EstadoSerializer(instance=estado)
        return Response(serializer.data)
        
class CiudadFilter(django_filters.rest_framework.FilterSet):
    """ 
    Filtro para Ciudades 
    """
    estadonombre = django_filters.CharFilter(name="estado__nombre", lookup_expr='icontains')
    class Meta:
        model = Ciudad
        fields = ['estado', 'estadonombre' ]    

class CiudadViewSet(viewsets.ModelViewSet):
    """ 
    Ciudades 
    """
    queryset = Ciudad.objects.all()
    serializer_class = CiudadSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = CiudadFilter
    ordering_fields = ('nombre', )

# class EstadoFilter(django_filters.rest_framework.FilterSet):
#     edo_ini = django_filters.NumberFilter(name="estado_id", lookup_expr='gte')
#     edo_fin = django_filters.NumberFilter(name="estado_id", lookup_expr='lte')

#     class Meta:
#         model = Estado
#         fields = ['pais', 'nombre', 'edo_ini', 'edo_fin']


# class EstadoViewSet(viewsets.ModelViewSet):
#     """ 
#     Estados 
#     """
#     queryset = Estado.objects.all()
#     serializer_class = EstadoSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filter_fields = ('pais',)

#     def get_queryset(self, *args, **kwargs):
        
#         try:
#             pais_busq = int(self.request.query_params.get('pais', None))
#         except:
#             pais_busq = None
            
#         # try:
#         #     nombre_busq = self.request.query_params.get('nombre', None)
#         # except:
#         #     nombre_busq = None
        
#         if pais_busq:            
#             qs = Estado.objects.filter(pais__exact=pais_busq)
#         else:
#             qs = Estado.objects.all()

        # if nombre_busq:        
        #     print(nombre_busq)    
        #     qs = Estado.objects.filter(codigo__icontains=nombre_busq)
        # else:
        #     qs = Estado.objects.all()

        # return qs.order_by('nombre')

    # filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # filter_class = EstadoFilter
    # ordering_fields = ('nombre', )

    # def list(self, request, *args, **kwargs):
        
    #     try:
    #         pais_busq = int(self.request.query_params.get('pais', None))
    #     except:
    #         pais_busq = None

         

    #     if pais_busq:
    #         print("pais_busq")
    #         print(pais_busq)
    #         queryset = Estado.objects.filter(pais__exact=pais_busq)
    #     else:
    #         queryset = Estado.objects.all()
 

    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    

# class EstadoViewSet(viewsets.ModelViewSet):
#     queryset = Estado.objects.all()
#     serializer_class = EstadoSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filter_fields = ('nombre')


# class CiudadViewSet(viewsets.ModelViewSet):
#     queryset = Ciudad.objects.all()
#     serializer_class = CiudadSerializer


# class UserExtensionViewSet(viewsets.ModelViewSet):
#     queryset = UserExtension.objects.all()
#     serializer_class = UserExtensionSerializer


class CiaViewSet(viewsets.ModelViewSet):
    queryset = Cia.objects.all()
    serializer_class = CiaSerializer


class CiaConsecutivoViewSet(viewsets.ModelViewSet):
    queryset = CiaConsecutivo.objects.all()
    serializer_class = CiaConsecutivoSerializer


class UserCiaViewSet(viewsets.ModelViewSet):
    queryset = UserCia.objects.all()
    serializer_class = UserCiaSerializer


class UserLogViewSet(viewsets.ModelViewSet):
    queryset = UserLog.objects.all()
    serializer_class = UserLogSerializer


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class PersonaJuridicaViewSet(viewsets.ModelViewSet):
    queryset = PersonaJuridica.objects.all()
    serializer_class = PersonaJuridicaSerializer


class PersonaNaturalViewSet(viewsets.ModelViewSet):
    queryset = PersonaNatural.objects.all()
    serializer_class = PersonaNaturalSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class DireccionViewSet(viewsets.ModelViewSet):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer


class SesionTrabajoViewSet(viewsets.ModelViewSet):
    queryset = SesionTrabajo.objects.all()
    serializer_class = SesionTrabajoSerializer

class DocRepFilter(django_filters.rest_framework.FilterSet):
    """ 
    Filtro para Docrep 
    """
    codigo = django_filters.CharFilter(name="det_docrepdets__producto__codigo", lookup_expr='icontains')
    class Meta:
        model = DocRep
        fields = ['codigo', ]    

class DocRepViewSet(viewsets.ModelViewSet):
    """ 
    Documentos de DocRep
    """
    queryset = DocRep.objects.all()
    serializer_class = DocRepSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = DocRepFilter


class DocRepDetViewSet(viewsets.ModelViewSet):
    queryset = DocRepDet.objects.all()
    serializer_class = DocRepDetSerializer


# Cia
# UserCia
# UserLog
# Persona
# PersonaJuridica
# PersonaNatural
# Producto
# Direccion
# SesionTrabajo
# DocRep
# DocRepDet

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
from datetime import datetime
from decimal import *
import pdb
# from dateutil import parser

from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

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

from ia.funciones import *
from django.db import transaction
from django.db.models import Q
import pytz
from rest_framework.exceptions import APIException

from django.utils.translation import ugettext as _
from django.core.cache import cache

import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors


from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
# from weasyprint import HTML
import pdfkit

from django.views.generic import View
from ia.funciones import render_to_pdf


# import fakeredis
# import simplejson
# import marshal
# import json

# Create your views here.

this_path = os.getcwd()


class InvalidAPIQuery(APIException):
    status_code = 400
    default_detail = _('An invalid query parameter was provided')


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

    def list(self, request):
        # cache = fakeredis.FakeStrictRedis()        
        # print("cache.get(Pais")
        # print(cache.get('estado'))
        # var1 = cache.get('estado')
        # var2 = simplejson.JSONDecoder(var1)
        # var2 = json.loads(var1)
        # var2 = var1.get(pk=4)
        # print("var2")
        # print(var2.codigo, var2.nombre)
        # for estado in var2:
        #     print(estado.nombre)
        # var3 = var2[0].nombre
        # print("var3")
        # print(var3)
        paises = Pais.objects.all()
        paisser = PaisSerializer(paises, many=True)
        return Response(paisser.data)


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
    ordering = ('estado_id')

    def list(self, request):
        # cache = fakeredis.FakeStrictRedis()
        estados = Estado.objects.all()
        edoser = EstadoSerializer(estados, many=True)
        # simplejson.loads(var1)
        # estadosjson = simplejson.JSONEncoder(estados)
        # objectBytes = marshal.dumps(estados)
        # objectBytes = json.dumps(estados)
        # cache.set('estado', estados)
        # print("cache.get(estado")
        # print(cache.get('estado'))
        return Response(edoser.data)

    def create(self, request):
        # print(request.user)

        mivar = "hola"
        try:
            # with transaction.atomic():
            var1 = 100
            var2 = 0
            # pais_id = request.data['pais_id']
            # pais = Pais.objects.get(pk=pais_id)  
            sistema_tz = pytz.timezone('UTC')
            mitz = pytz.timezone('EST')
            fecha = request.data['fecha']
            # objFecha = parser.parse(fecha)
            objfecha = strToDatetime(fecha)
            objfecha2 = objfecha.replace(tzinfo=mitz)
            objfecha3 = objfecha.astimezone(sistema_tz)
            # print("objFecha")
            # print(objFecha)
            # print("objFecha2")
            # print(objFecha2)
            # print("objFecha3")
            # print(objFecha3)
            # pdb.set_trace()
            # print(objFecha.astimezone(miTZ))
            # print("Tipo de Fecha")
            # print(type(objFecha))

            # raise Exception

            # pais = Pais.objects.create(
            #     nombre="Pais error444",
            #     codigo="Pe4")
            # pais.save()

            # numero = 0
            # error = 'error inicial'
            # retorno = {}

            # retorno = {'error': '', 'numero': 0, 'status': 1}

            retorno = consecutivo_doc(1, 4)
            print("retorno en el view")
            print(retorno)
            print("retorno.numero")
            print(retorno['numero'])
            if retorno['status'] == -1:
                raise InvalidAPIQuery(retorno['error'])

            # print("Error en consecutivo_doc")
            # print(error)
            # print("numero")
            # print(numero)

            #     raise InvalidAPIQuery(as_error)
            # else:                
            # print("Numero")
            # print(retorno.numero)
            
            numero = retorno['numero']

            costonum = float(numero)
            estado = Estado.objects.create(
                nombre=request.data['nombre'],
                codigo=request.data['codigo'],
                fecha=objfecha2,
                # costo=request.data['costo'],
                costo=costonum,
                activo=request.data['activo'],
                pais_id=request.data['pais_id']
            )  
            # estado = Estado.objects.create(request.data)
            # var3 = midivision(100, 0)
            serializer = EstadoSerializer(instance=estado)

            return Response(serializer.data)

        except Exception as e:
            # raise InvalidAPIQuery(str(e))
            # if as_error == '':  
            print("mivar")     
            print(mivar)          
            raise InvalidAPIQuery(
                _('Error Creando el estado. ') + request.data['nombre'] + ' ' + mivar + ' ' + str(e))
            # else:
            #     raise InvalidAPIQuery(as_error)

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

    # @transaction.atomic
    def create(self, request):
        
        try:
            
            # with transaction.atomic():
         
            cia_id = request.data['cia_id']
            persona_id = request.data['persona_id']
            direccion_id = request.data['direccion_id']
            ucrea_id = request.data['ucrea_id']
            origen_id = request.data['origen_id']

            tipo_documento = request.data['tipo_documento']
            credito = request.data['credito']
            dias_credito = request.data['dias_credito']
            fecha_emision = request.data['fecha_emision']
            fecha_vencimiento = request.data['fecha_vencimiento']
            subtotal = request.data['subtotal']
            impuesto = request.data['impuesto']
            total = request.data['total']
            observaciones = request.data['observaciones']

            # cia = Cia.objects.get(pk=cia_id)   
            # persona = Persona.objects.get(pk=persona_id)   
            # direccion = Direccion.objects.get(pk=direccion_id)   
            # ucrea = Usuario.objects.get(pk=ucrea_id)   
            # origen = DocRep.objects.get(pk=origen_id)   
            
            numero = consecutivo_doc(cia_id, tipo_documento)
                
            docrep = DocRep.objects.create(
                tipo_documento=tipo_documento,
                numero=numero,
                credito=credito,
                dias_credito=dias_credito,
                fecha_emision=fecha_emision,
                fecha_vencimiento=fecha_vencimiento,
                subtotal=subtotal,
                impuesto=impuesto,
                total=total,
                observaciones=observaciones,
                cia_id=cia_id,
                persona_id=persona_id,
                direccion_id=direccion_id,
                ucrea_id=ucrea_id,
                origen_id=origen_id
            )

            serializer = DocRepSerializer(instance=docrep)
            return Response(serializer.data)

        except Exception as e:
            raise e

    # @transaction.atomic
    def update(self, request, pk):
        
        try:
            
            # with transaction.atomic():
                          
            persona_id = request.data['persona_id']
            direccion_id = request.data['direccion_id']                
            origen_id = request.data['origen_id']
            
            credito = request.data['credito']
            dias_credito = request.data['dias_credito']
            fecha_emision = request.data['fecha_emision']
            fecha_vencimiento = request.data['fecha_vencimiento']
            subtotal = request.data['subtotal']
            impuesto = request.data['impuesto']
            total = request.data['total']
            observaciones = request.data['observaciones']
                
            # persona = Persona.objects.get(pk=persona_id)   
            # direccion = Direccion.objects.get(pk=direccion_id)                   
            # origen = DocRep.objects.get(pk=origen_id)   
            
            docrep = DocRep.objects.get(pk=pk)

            # cia = Cia.objects.get(pk=docrep.cia)   
            # ucrea = Usuario.objects.get(pk=docrep.ucrea)
            # uaprueba = Usuario.objects.get(pk=docrep.uaprueba)
            # uanula = Usuario.objects.get(pk=docrep.uanula)
            # ufactura = Usuario.objects.get(pk=docrep.ufactura)

            docrep.credito = credito
            docrep.dias_credito = dias_credito
            docrep.fecha_emision = fecha_emision
            docrep.fecha_vencimiento = fecha_vencimiento
            docrep.subtotal = subtotal
            docrep.impuesto = impuesto
            docrep.total = total
            docrep.observaciones = observaciones

            # docrep.cia_id = cia_id
            docrep.persona_id = persona_id
            docrep.direccion_id = direccion_id
            # docrep.ucrea_id = ucrea_id
            docrep.origen_id = origen_id                

            docrep.save()

            serializer = DocRepSerializer(instance=docrep)
            return Response(serializer.data)
                    
        except Exception as e:
            raise e


class DocRepDetViewSet(viewsets.ModelViewSet):
    queryset = DocRepDet.objects.all()
    serializer_class = DocRepDetSerializer


def reporte(request):
    # Crea el HttpResponse header con PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="jt-report.pdf"'

    # Crea el objeto pdf
    # buffer = BytesIO()
    # c = canvas.Canvas(buffer, pagesize=A4)
    c = canvas.Canvas(response)
    # Header
    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawString(30, 750, 'Infoauto')
    c.setFont('Helvetica', 12)
    c.drawString(30, 737, 'Reporte')
    c.setFont('Helvetica-Bold', 12)
    c.drawString(450, 750, '25/05/2017')
    c.line(440, 747, 520, 747)

    # c.save()
    # pdf = buffer.close()
    # response.write(pdf)
    # Close the PDF object cleanly, and we're done.
    c.showPage()
    c.save()
    return response


def report2(request):
    # If you’re creating a complex PDF document with ReportLab,
    # consider using the io library as a temporary holding place for your PDF file.
    # This library provides a file-like object interface that is particularly efficient.
    # Here’s the above “Hello World” example rewritten to use io:

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="t-report2.pdf.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    c = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    c.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
    c.showPage()
    c.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


# def estado_to_pdf_view(request):

#     pais_id = 1
#     pais = Pais.objects.get(pk=pais_id)
#     estados = Estado.objects.filter(pais_id__exact=pais_id).order_by('nombre')
#
#     data = {'estados': estados, 'pais': pais}
#     pdf = render_to_pdf('estado_pdf.html', data)
#     return HttpResponse(pdf, content_type='application/pdf')


# def estado_to_pdf_view(request):
#     # con xhtml2pdf
#     pais_id = 1
#     pais = Pais.objects.get(pk=pais_id)
#     estados = Estado.objects.filter(pais_id__exact=pais_id).order_by('nombre')
#
#     # template = get_template('estado_pdf.html')
#     context = {'estados': estados, 'pais': pais}
#     # html = template.render(context)
#     pdf = render_to_pdf('estado_pdf.html', context)
#     if pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         filename = "Estados_de_%s.pdf" % pais
#         content = "inline; filename='%s'" % filename
#         download = request.GET.get("download")
#         if download:
#             content = "attachment; filename='%s'" % filename
#         response['Content-Disposition'] = content
#         return response
#     return HttpResponse("Not found")

# class GeneratePdf(View):
#
#     def get(self, request, *args, **kwargs):
#         pais_id = 1
#         pais = Pais.objects.get(pk=pais_id)
#         estados = Estado.objects.filter(pais_id__exact=pais_id).order_by('nombre')
#
#         data = {'estados': estados, 'pais': pais}
#         pdf = render_to_pdf('pdf_template.html', data)
#         return HttpResponse(pdf, content_type='application/pdf')
#
#
# class GeneratePDF(View):
#
#     def get(self, request, *args, **kwargs):
#
#         pais_id = 1
#         pais = Pais.objects.get(pk=pais_id)
#         estados = Estado.objects.filter(pais_id__exact=pais_id).order_by('nombre')
#
#         template = get_template('pdf_template.html')
#         context = {'estados': estados, 'pais': pais}
#         html = template.render(context)
#         pdf = render_to_pdf('pdf_template.html', context)
#         if pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             filename = "Invoice_%s.pdf" %("12341231")
#             content = "inline; filename='%s'" %(filename)
#             download = request.GET.get("download")
#             if download:
#                 content = "attachment; filename='%s'" %(filename)
#             response['Content-Disposition'] = content
#             return response
#         return HttpResponse("Not found")

def estado_to_html(request):
    pais_id = 1
    pais = Pais.objects.get(pk=pais_id)
    estados = Estado.objects.filter(pais_id__exact=pais_id).order_by('nombre')

    content = render_to_string('estado_b_pdf.html', {'estados': estados, 'pais': pais})
    response = HttpResponse(content)
    return response


def estado_to_pdf_view(request):
    # pdfkit
    options = {
        'page-size': 'A4',
        'margin-top': '0.55in',
        'margin-right': '0.55in',
        'margin-bottom': '0.55in',
        'margin-left': '0.55in',
        'encoding': "UTF-8",
        # any other wkhtmltopdf options
    }

    pais_id = 1
    pais = Pais.objects.get(pk=pais_id)
    estados = Estado.objects.filter(pais_id__exact=pais_id).order_by('nombre')

    # content = render_to_string(
    #     'pdf_template.html', {
    #         'contents': some_your_html
    #     }
    # )
    # file_html = 'estado_pdf.html'
    # print("file_html")
    # print(file_html)
    content = render_to_string('estado_b_pdf.html', {'estados': estados, 'pais': pais})
    # response = HttpResponse(content)

    pdf = pdfkit.PDFKit(content, "string", options=options).to_pdf()

    response = HttpResponse(pdf)
    response['Content-Type'] = 'application/pdf'
    # change attachment to inline if you want open file in browser tab instead downloading
    response['Content-disposition'] = 'attachment;filename={}.pdf'.format('estado_pdf.pdf')

    return response

# def estado_to_pdf_view(request):
#     # paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
#     # html_string = render_to_string('core/pdf_template.html', {'paragraphs': paragraphs})
#
#     pais_id = 1
#     pais = Pais.objects.get(pk=pais_id)
#     estados = Estado.objects.filter(pais_id__exact=pais_id).order_by('nombre')
#     html_string = render_to_string('ia/estado_pdf.html', {'estados': estados, 'pais': pais})
#     html = HTML(string=html_string)
#     html.write_pdf(target='/tmp/estado_pdf.pdf')
#
#     fs = FileSystemStorage('/tmp')
#     with fs.open('estado_pdf.pdf') as pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="estado_pdf.pdf"'
#         return response
#
#     return response




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

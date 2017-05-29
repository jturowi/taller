"""


///////////////////////////////////////////////////////////////////////////////////////////////
                                        DUDAS PENDIENTES
///////////////////////////////////////////////////////////////////////////////////////////////
29-05-2017
Como subir y bajar archivos (pdf, imagenes, videos)




///////////////////////////////////////////////////////////////////////////////////////////////
Porque ha veces se toca el create en el serializador y no en la vista

Debug

# Serializer: Formatos de fecha y decimales 

# Pendiente ejemplo para manejo de fechas con zona tanto de evio como de recepcion

#Localizacion de mensaje de error del sistema y los propios del API personalizado

#django-admin makemessages -l es
#django-admin makemessages -l en
#manage.py compilemessages -l es
#manage.py compilemessages -l en

# Manejo de transacciones

# Manejo de errores dentro de una transaccion

Funcion Generica que le pases una instancia de objeto modelo y lo llene con el request.data


Guardas datos del ambiente del usuario y sesion
    diccionario general
    diccionario por cia
    diccionario por departamento


Eventos de seguridad para acciones por usuario, departamento y ventana
    Aprobar un pedido
    facturar un pedido
    Anular un pedido


Crear Diccionario en el cache en una funcion

Leer Diccionario en el cache en una funcion
   

https://github.com/rgl/redis/downloads

   
        
///////////////////////////////////////////////////////////////////////////////////////////////
                                        DUDAS RESUELTAS
///////////////////////////////////////////////////////////////////////////////////////////////

# import pytz
    # import datetime

    # >>> utc =pytz.timezone('UTC')
    # >>> 
    # >>> datetime.datetime(2017, 5, 9, 12, 0, tzinfo=utc)
    # datetime.datetime(2017, 5, 9, 12, 0, tzinfo=<UTC>)
    # >>> print(datetime)
    # <module 'datetime' from 'C:\\Users\\josepc\\AppData\\Local\\Programs\\Python\\Python36\\lib\\datetime.py'>
    # >>> fecha1 = datetime.datetime(2017, 5, 9, 12, 0, tzinfo=utc)
    # >>> print(fecha1)
    # 2017-05-09 12:00:00+00:00
    # >>> est = pytz.timezone('US/Eastern')
    # >>> fecha2 = fecha1.astimezone(est)
    # >>> print(fecha1)
    # 2017-05-09 12:00:00+00:00
    # >>> print(fecha2)
    # 2017-05-09 08:00:00-04:00  
 
        
jira control de versiones:
https://www.atlassian.com/software/jira?_mid=8789c40461a1b4067bb573d55bfba564&aceid=&adposition=1t1&adgroup=38294495269&campaign=742611005&creative=174457531916&device=c&keyword=jira&matchtype=e&network=g&placement=&gclid=CjsKDwjw0cXIBRCxjqnE3K3sHhIkAL1LezSiZ8SCg4fV0PuP6emI_8r43KkxwjsRKBHcinPij5gSGgK9f_D_BwE&gclsrc=aw.ds

jenkis:
https://jenkins.io

http://docs.celeryproject.org/en/latest/django/

https://redis.io

docker run --name redis_taller  –p 6379:6379 redis


pip install django-redis

# Choice pueden ser dinamicos?

https://niwinz.github.io/django-redis/latest/#_infinite_timeout

install simplejson

"""
import fakeredis
CACHES = {
    "default": {
        "OPTIONS": {
            "REDIS_CLIENT_CLASS": "fakeredis.FakeStrictRedis",
        }
    }
}
"""


Crear Aplicaciones -- Estructura del Proyecto y las aplicaciones

Control de proyecto y versiones

En admin como relacionar una direccion a una persona en la lista de seleccion



# Pasar parametros y leerlos y que sirvan de filtros en el select ( en estados buscar los de un pais)

# Filter y query_set

# No hace el hash del password en admin


ADMINSITRACION
    CXC
    CXP
    BANCOS
    CONTABILIDAD
    AF

REPUESTO
    COMPRAS
    VENTAS
    TRANSFERENCIA
    INVENTARIO

SERVICIO
    CITAS
    TRANSFERENCIA
    OS

VEHICULO
    COMPRA
    VTA
    TRANSFERENCIA
    INVENTARIO

PRINCIPAL
    SEGURIDAD
    PARAMETROS
    CONFIGURACIONES

INStALACION DE REDIS
https://github.com/MSOpenTech/redis/releases

redis-server.exe

redis-cli.exe ping
y hacer ping >>> PONG

"""

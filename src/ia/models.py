from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

tipos_15 = (
        (0, 'N/A'),
        (1, 'Factura'),
        (2, 'Nota de Débito'),
        (3, 'Nota de Crédito'),        
        (4,	'Pedido'),
        (5,	'Cotización'),
        (6,	'Solicitud de Devolución'),
        (7,	'Solicitud de Nota de Crédito'),
        (8,	'Solicitud de Nota de Débito'),
        (9,	'Devolución de Mercancía'),
        (10, 'Orden TOT'),
        (11, 'NO USADA'),
        (12, 'Orden de Compra'),
        (13, 'Solicitud de Cotización'),
        (14, 'Nota de Entrega'),
        (15, 'Recepción'),
        (16, 'Cierre de Inventario'),
        (17, 'Nota de Entrada al Inventario'),
        (18, 'Nota de Salida al Inventario'),
        (19, 'Transferencia'),
        (20, 'Devolución de Transferencia'),
        (21, 'Solicitud de Transferencia'),
        (22, 'Solicitud de Devolución de Transferencia'),
        (23, 'Cotización de O/S'),
        (24, 'Orden de Servicio'),
        (25, 'Reclamo de Garantía'),
        (26, 'Prefactura'),
        (27, 'Anticipo'),
        (28, 'Cheque Devuelto'),
        (29, 'Giro'),
        (30, 'Nota de Débito por Mora'),
        (31, 'Reclamo de Devolución'),
        (32, 'Cheque')
    )




class UsuarioManager(BaseUserManager):
    """Class required by Django for managing our users from the management
    command.
    """

    def create_user(self, email, name, password=None):
        """Creates a new user with the given detials."""

        # Check that the user provided an email.
        if not email:
            raise ValueError('Users must have an email address.')

        # Create a new user object.
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        # Set the users password. We use this to create a password
        # hash instead of storing it in clear text.
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creates and saves a new superuser with given detials."""

        # Create a new user with the function we created above.
        user = self.create_user(
            email,
            name,
            password
        )

        # Make this user an admin.
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    """A user profile in our system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    nombre = models.CharField(max_length=60, blank=True)
    apellido = models.CharField(max_length=100, blank=True)     
    tipo = models.PositiveSmallIntegerField(default=0)    
    genero_codigo = models.BooleanField(default=False)
    codigo_gen = models.IntegerField(null=True, blank=True)
    fecha_gen = models.DateField(null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=128)
    cia = models.ForeignKey('Cia', related_name='cias', null=True, blank=True, on_delete=models.PROTECT)
    tz = models.CharField(max_length=40, blank=True)  


 
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
 
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = "usuario"

    def get_full_name(self):
        """
        Required function so Django knows what to use as the users full name.
        """

        self.nombre + ' ' + self.apellido

    def get_short_name(self):
        """
        Required function so Django knows what to use as the users short name.
        """

        self.name

    def __str__(self):
        """What to show when we output an object as a string."""

        return self.email    
    
class Pais(models.Model):
    pais_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150,  blank=False, unique=True)
    codigo = models.CharField(max_length=6,  blank=False)

    class Meta:
        db_table = "pais"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre   

class Estado(models.Model):
    estado_id = models.BigAutoField(primary_key=True)
    pais = models.ForeignKey(Pais, related_name='estados', null=False, blank=False, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=150,  blank=False)
    codigo = models.CharField(max_length=6,  blank=False)

    class Meta:
        db_table = "estado"
        ordering = ['nombre']

        unique_together = [
            "pais", "nombre"
        ]

    def __str__(self):
        return self.nombre

class Ciudad(models.Model):
    ciudad_id = models.BigAutoField(primary_key=True) 
    estado = models.ForeignKey('Estado', related_name='ciudades', null=False, blank=False, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=150,  blank=False)
    codigo = models.CharField(max_length=6,  blank=False)

    class Meta:
        db_table = "ciudad"
        ordering = ['nombre']
        unique_together = [
            "estado", "nombre"
        ]

    def __str__(self):
        return self.nombre

class Cia(models.Model):
    cia_id = models.BigAutoField(primary_key=True)  
    razon_social = models.CharField(max_length=250, null=False, blank=False, unique=True) 
    rif = models.CharField(max_length=35,  blank=False, unique=True)  

    class Meta:
        db_table = "cia"
        ordering = ['razon_social']

    def __str__(self):
        return self.razon_social   

class CiaConsecutivo(models.Model):    
    ciaconsecutivo_id = models.BigAutoField(primary_key=True) 
    cia = models.ForeignKey('Cia', related_name='ciaconsecutivos', null=False, blank=False, on_delete=models.PROTECT) 
    tipo_documento = models.PositiveSmallIntegerField(default=0)  
    numero = models.IntegerField(default=0)  

    class Meta:
        db_table = "cia_consecutivo"  
        ordering = ['cia', 'tipo_documento']
        unique_together = [
                "cia", "tipo_documento"
            ]
    
class UserCia(models.Model):
    user_cia_id = models.BigAutoField(primary_key=True)  
    cia = models.ForeignKey('Cia', related_name='cia_usercias', null=False, blank=False, on_delete=models.PROTECT)   
    usuario = models.ForeignKey('Usuario', related_name='u_usercias', null=True, blank=False, on_delete=models.PROTECT)   
    tipo_usuario = models.PositiveSmallIntegerField(default=0) 

    class Meta:
        db_table = "user_cia"

class UserLog(models.Model):
    user_log_id = models.BigAutoField(primary_key=True)  
    cia = models.ForeignKey('Cia', related_name='cia_userlogs', null=False, blank=False, on_delete=models.PROTECT)   
    usuario = models.ForeignKey('Usuario', related_name='u_userlogs', null=False, blank=False, on_delete=models.PROTECT)       
    fecha = models.DateTimeField(null=False, blank=False)
    sesion = models.CharField(max_length=512,  blank=False)   

    class Meta:
        db_table = "user_log" 

class Persona(models.Model):
    persona_id = models.BigAutoField(primary_key=True)  
    cia = models.ForeignKey('Cia', related_name='personas', null=False, blank=False, on_delete=models.PROTECT)   
    nombre = models.CharField(max_length=150,  blank=False)        
    apellido = models.CharField(max_length=150, null=True, blank=True)        
    cedula_rif = models.CharField(max_length=35,  blank=False, unique=True)   
    juridica = models.BooleanField() 
    activo = models.BooleanField()  
    bloqueado = models.BooleanField()          
    ultima_operacion = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        db_table = "persona" 
        ordering = ['cedula_rif']
        unique_together = [
                "cia", "cedula_rif"
            ]

    def __str__(self):
        return self.nombre   


class PersonaJuridica(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.PROTECT) 
    registro_mercantil = models.CharField(max_length=60) 
    nro_registro = models.CharField(max_length=10)
    tomo = models.CharField(max_length=6) 
    fecha_registro = models.DateTimeField() 

    class Meta:
        db_table = "persona_juridica"    

class PersonaNatural(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.PROTECT) 
    razon_social = models.CharField(max_length=200, null=True, blank=True) 
    rif = models.CharField(max_length=35, null=True, blank=True) 
    fecha_nacimiento = models.DateTimeField(null=True, blank=True)    
    sexo = models.PositiveSmallIntegerField(default=0) 
    estado_civil = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "persona_natural"     

class Producto(models.Model):
    producto_id = models.BigAutoField(primary_key=True)  
    cia = models.ForeignKey('Cia', related_name='productos', null=False, blank=False, on_delete=models.PROTECT) 
    codigo = models.CharField(max_length=35, null=False, blank=False)
    descripcion = models.CharField(max_length=35, null=False, blank=False)  
    precio = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    costo = models.DecimalField(max_digits=18, decimal_places=6, default=0) 
    existencia = models.DecimalField(max_digits=18, decimal_places=2, default=0)  
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "producto"   
        ordering = ['codigo']
        unique_together = [
                "cia", "codigo"
            ]

    def __str__(self):
        return self.codigo 
  
class Direccion(models.Model):
    direccion_id = models.BigAutoField(primary_key=True) 
    persona = models.ForeignKey('Persona', related_name='p_direcciones', null=False, blank=False, on_delete=models.PROTECT)    
    ciudad = models.ForeignKey('Ciudad', related_name='c_direcciones', null=False, blank=False, on_delete=models.PROTECT) 
    estado = models.ForeignKey('Estado', related_name='e_direcciones', null=False, blank=False, on_delete=models.PROTECT)    
    pais = models.ForeignKey('Pais', related_name='p_direcciones', null=False, blank=False, on_delete=models.PROTECT)            
    direccion = models.TextField()
    direccion_completa = models.TextField()

    class Meta:
        db_table = "direccion"   

    def __str__(self):
        return self.direccion_completa        

class SesionTrabajo(models.Model):
    sesion_id = models.BigAutoField(primary_key=True) 
    mitoken = models.CharField(max_length=512, null=False, blank=False, unique=True)  
    cia = models.ForeignKey('Cia', related_name='c_sesiontrabajos', null=True, blank=False, on_delete=models.PROTECT) 
    usuario = models.ForeignKey(Usuario, related_name='u_sesiontrabajos', null=False, blank=False, on_delete=models.PROTECT) 
    parametros = models.TextField(null=True, blank=True)  

    class Meta:
        db_table = "sesion_trabajo"  



class DocRep(models.Model):
    
    docrep_id = models.BigAutoField(primary_key=True) 
    cia = models.ForeignKey('Cia', related_name='c_docreps', null=False, blank=False, on_delete=models.PROTECT) 
    persona = models.ForeignKey('Persona', related_name='p_docreps', null=False, blank=False, on_delete=models.PROTECT)
    direccion = models.ForeignKey('Direccion', related_name='dir_docreps', null=False, blank=False, on_delete=models.PROTECT)  
    # ucrea = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ucrea_docreps', null=False, blank=False, on_delete=models.PROTECT)   
    ucrea = models.ForeignKey('Usuario', related_name='ucrea_docreps', null=False, blank=False, on_delete=models.PROTECT)   
    uaprueba = models.ForeignKey('Usuario', related_name='uapro_docreps', null=True, blank=True, on_delete=models.PROTECT)
    uanula = models.ForeignKey('Usuario', related_name='uanu_docreps', null=True, blank=True, on_delete=models.PROTECT)  
    ufactura = models.ForeignKey('Usuario', related_name='ufact_docreps', null=True, blank=True, on_delete=models.PROTECT)  
    origen = models.ForeignKey('DocRep', related_name='orig_docreps', null=True, blank=True, on_delete=models.PROTECT)  
    tipo_documento = models.PositiveSmallIntegerField(choices=tipos_15, default=0)  
    numero = models.CharField(max_length=35) 
    credito = models.BooleanField(default=False)
    dias_credito = models.PositiveSmallIntegerField(default=0)  
    fecha_emision = models.DateTimeField()
    fecha_vencimiento = models.DateTimeField() 
    fecha_anulacion = models.DateTimeField(null=True, blank=True)  
    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)  
    observaciones = models.TextField(null=True, blank=True)

    class Meta:         
        db_table = "doc_rep"  
        ordering = ['numero']
         

    def __str__(self):
        return self.numero         

class DocRepDet(models.Model):
    docrepdet_id = models.BigAutoField(primary_key=True) 
    docrep = models.ForeignKey('DocRep', related_name='det_docrepdets', null=False, blank=False, on_delete=models.PROTECT)  
    producto = models.ForeignKey('Producto', related_name='prod_docrepdets', null=True, blank=False, on_delete=models.PROTECT) 
    cantidad = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=18, decimal_places=2, default=0)    
    costo = models.DecimalField(max_digits=18, decimal_places=6, default=0) 

    class Meta:         
        db_table = "doc_rep_det"  


class Perfil(models.Model):
    perfil_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:         
        db_table = "perfil"  

class Ventana(models.Model):
    ventana_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:         
        db_table = "ventana"  

class UserPerfil(models.Model):
    userperfil_id = models.BigAutoField(primary_key=True) 
    usuario = models.ForeignKey('Usuario', related_name='up_usuarios', null=False, blank=False, on_delete=models.PROTECT) 
    perfil = models.ForeignKey('Perfil', related_name='up_perfiles', null=False, blank=False, on_delete=models.PROTECT) 

    class Meta:         
        db_table = "userperfil" 

        unique_together = [
                "usuario", "perfil"
            ]

class PerfilDet(models.Model):
    perfildet_id = models.BigAutoField(primary_key=True)
    perfil = models.ForeignKey('Perfil', related_name='det_perfiles', null=False, blank=False, on_delete=models.PROTECT) 
    ventana = models.ForeignKey('Ventana', related_name='det_ventanas', null=False, blank=False, on_delete=models.PROTECT) 
    evento = models.CharField(max_length=100, null=False, blank=False)


    class Meta:         
        db_table = "perfildet"  
        unique_together = [
               "ventana", "perfil", "evento"
            ]
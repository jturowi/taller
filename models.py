from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class UserExtension(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.PositiveSmallIntegerField(default=0)
    bloqueado = models.BooleanField(default=False)
    genero_codigo = models.BooleanField(default=False)
    codigo_gen = models.IntegerField()
    fecha_gen = models.DateField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    

class Ciudad(models.Model):
    ciudad_id = models.BigAutoField(primary_key=True) 
    estado = models.ForeignKey('Estado', related_name='estadociudad', null=False, blank=False)
    nombre = models.CharField(max_length=150,  blank=False)
    codigo = models.CharField(max_length=6,  blank=False)

    class Meta:
        ordering = ['nombre']
        unique_together = [
            "estado", "nombre"
        ]

    def __str__(self):
        return self.nombre

class Estado(models.Model):
    estado_id = models.BigAutoField(primary_key=True)
    pais = models.ForeignKey('Pais', related_name='paises', null=False, blank=False)
    nombre = models.CharField(max_length=150,  blank=False)
    codigo = models.CharField(max_length=6,  blank=False)

    class Meta:
        ordering = ['nombre']

        unique_together = [
            "pais", "nombre"
        ]

    def __str__(self):
        return self.nombre

class Pais(models.Model):
    pais_id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150,  blank=False, unique=True)
    codigo = models.CharField(max_length=6,  blank=False)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre   

class Cia(models.Model):
    cia_id = models.BigAutoField(primary_key=True)  
    razon_social = models.CharField(max_length=250,  blank=False, unique=True) 
    rif = models.CharField(max_length=35,  blank=False, unique=True)  

    class Meta:
        ordering = ['razon_social']

    def __str__(self):
        return self.razon_social   

class UserCia(models.Model):
    user_cia_id = models.BigAutoField(primary_key=True)  
    cia = models.ForeignKey('Cia', related_name='Ciausercia', null=True, blank=False)   
    # usuario = models.ForeignKey('User', related_name='UseruserCia', null=True, blank=False)   
    tipo_usuario = models.PositiveSmallIntegerField(default=0) 

class UserLog(models.Model):
    user_log_id = models.BigAutoField(primary_key=True)  
    cia = models.ForeignKey('Cia', related_name='Ciauserlog', null=True, blank=False)   
    # usuario = models.ForeignKey('User', related_name='UserLogs', null=False, blank=False)       
    fecha = models.DateTimeField(null=False, blank=False)
    sesion = models.CharField(max_length=512,  blank=False)    

class Persona(models.Model):
    persona_id = models.BigAutoField(primary_key=True)  
    cia = models.ForeignKey('Cia', related_name='Ciapersona', null=True, blank=False)   
    nombre = models.CharField(max_length=150,  blank=False)        
    apellido = models.CharField(max_length=150,  blank=False)        
    cedula_rif = models.CharField(max_length=35,  blank=False, unique=True)   
    juridica = models.BooleanField() 
    activo = models.BooleanField()  
    bloqueado = models.BooleanField()          
    ultima_operacion = models.DateTimeField()
    email = models.EmailField()
    email_alterno = models.EmailField()

    class Meta:
        ordering = ['cedula_rif']
        unique_together = [
                "cia", "cedula_rif"
            ]

        def __str__(self):
            return self.cedula_rif 


class PersonaJuridica(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE) 
    registro_mercantil = models.CharField(max_length=60) 
    nro_registro = models.CharField(max_length=10)
    tomo = models.CharField(max_length=6) 
    fecha_registro = models.DateTimeField()    

class PersonaNatural(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE) 
    razon_social = models.CharField(max_length=200) 
    rif = models.CharField(max_length=35) 
    nit = models.CharField(max_length=35)    
    fecha_nacimiento = models.DateTimeField() 
    fecha_boda = models.DateTimeField()   
    sexo = models.PositiveSmallIntegerField(default=0) 
    estado_civil = models.PositiveSmallIntegerField(default=0)  
    hijos = models.PositiveSmallIntegerField(default=0)  
    hijos_varones = models.PositiveSmallIntegerField(default=0) 

class Producto(models.Model):
    producto_id = models.BigAutoField(primary_key=True)  
    cia = models.ForeignKey('Cia', related_name='Cias', null=True, blank=False) 
    codigo = models.CharField(max_length=35, null=False, blank=False)
    descripcion = models.CharField(max_length=35, null=False, blank=False)  
    precio = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    costo = models.DecimalField(max_digits=18, decimal_places=6, default=0) 
    existencia = models.DecimalField(max_digits=18, decimal_places=2, default=0)  
    observaciones = models.TextField()

    class Meta:
        ordering = ['codigo']
        unique_together = [
                "cia", "codigo"
            ]

        def __str__(self):
            return self.codigo 
  
class Direccion(models.Model):
    direccion_id = models.BigAutoField(primary_key=True) 
    persona = models.ForeignKey('Persona', related_name='Personas', null=False, blank=False)    
    ciudad = models.ForeignKey('Ciudad', related_name='Ciudades', null=False, blank=False) 
    estado = models.ForeignKey('Estado', related_name='Estados', null=False, blank=False)    
    pais = models.ForeignKey('Pais', related_name='Paises', null=False, blank=False)            
    direccion = models.TextField()
    direccion_completa = models.TextField()


class SesionTrabajo(models.Model):
    sesion_id = models.BigAutoField(primary_key=True) 
    mitoken = models.CharField(max_length=512, null=False, blank=False, unique=True)  
    cia = models.ForeignKey('Cia', related_name='Ciasesiontrab', null=True, blank=False) 
    # usuario = models.ForeignKey('User', related_name='Usuarios', null=False, blank=False) 
    parametros = models.TextField()  

class DocRep(models.Model):
    docrep_id = models.BigAutoField(primary_key=True) 
    cia = models.ForeignKey('Cia', related_name='Ciadocrep', null=True, blank=False) 
    persona = models.ForeignKey('Persona', related_name='Personadocrep', null=True, blank=False)
    direccion = models.ForeignKey('Direccion', related_name='Direcciones', null=True, blank=False)  
    # ucrea = models.ForeignKey('User', related_name='Creados', null=False, blank=False)   
    # uaprueba = models.ForeignKey('User', related_name='Aprobados')
    # uanula = models.ForeignKey('User', related_name='Anulados')  
    # ufactura = models.ForeignKey('User', related_name='Facturados')  
    origen = models.ForeignKey('DocRep', related_name='Origenes', null=True, blank=False)  
    tipo_documento = models.PositiveSmallIntegerField(default=0)  
    numero = models.CharField(max_length=35) 
    credito = models.BooleanField(default=False)
    dias_credito = models.PositiveSmallIntegerField(default=0)  
    fecha_emision = models.DateTimeField()
    fecha_vencimiento = models.DateTimeField() 
    fecha_anulacion = models.DateTimeField()  
    subtotal = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)  
    observaciones = models.TextField()

    class Meta:
        ordering = ['numero']
         

        def __str__(self):
            return self.numero         

class DocRepDet(models.Model):
    docrepdet_id = models.BigAutoField(primary_key=True) 
    docrep = models.ForeignKey('DocRep', related_name='DocReps', null=True, blank=False)  
    producto = models.ForeignKey('Producto', related_name='Productos', null=True, blank=False) 
    cantidad = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=18, decimal_places=2, default=0)    
    costo = models.DecimalField(max_digits=18, decimal_places=6, default=0) 


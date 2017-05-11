from django.contrib.auth.models import Group

from rest_framework import serializers

from ia.models import Pais, Estado, Ciudad, Usuario
from ia.models import Cia, UserCia, UserLog, Persona, PersonaJuridica, PersonaNatural
from ia.models import Producto, Direccion, SesionTrabajo, DocRep, DocRepDet, CiaConsecutivo

""" 
	Comentario 
"""
# ModelSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    """A serializer for our usuario object."""

    class Meta:
        model = Usuario
        fields = ('id', 'email', 'name', 'is_active', 'is_staff', 'tipo', 'nombre', 
                    'apellido', 'genero_codigo', 'codigo_gen', 'fecha_gen', 'fecha_nacimiento',
                    'last_login', 'password', 'token', 'cia')
        extra_kwargs = {
            'last_login': {'read_only': True},
            'genero_codigo': {'read_only': True},
            'codigo_gen': {'read_only': True},
            'fecha_gen': {'read_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """Used to create a new user."""

        user = Usuario(
            email=validated_data['email'],
            name=validated_data['name'],
            is_active=validated_data['is_active'],            
            tipo=validated_data['tipo'],
            nombre=validated_data['nombre'],
            apellido=validated_data['apellido'],            
            fecha_nacimiento=validated_data['fecha_nacimiento'],                        
        )

        user.set_password(validated_data['password'])
        user.save()
        return user




# class UserSerializer(serializers.ModelSerializer):    
# 	class Meta:
# 		model = User
# 		fields = ['username', 'email', 'groups']

class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ['name']

class PaisSerializer(serializers.ModelSerializer):
	class Meta:
		model = Pais
		fields = ['pais_id', 'nombre', 'codigo']

class EstadoSerializer(serializers.ModelSerializer):
    pais = PaisSerializer(required=True, many=False)
    #pais = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Estado
        fields = ['estado_id', 'nombre', 'codigo', 'pais']
        depth = 1

class CiudadSerializer(serializers.ModelSerializer):
	# estado = EstadoSerializer(many=False, read_only=True)
	class Meta:
		model = Ciudad
		fields = ['ciudad_id', 'nombre', 'estado']
		# read_only_fields = ('estado', )

# class UserExtensionSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = UserExtension
# 		fields = ['usuario', 'tipo', 'bloqueado', 'genero_codigo', 'codigo_gen', 'fecha_gen', 'birth_date']

class CiaConsecutivoSerializer(serializers.ModelSerializer):
	class Meta:
		model = CiaConsecutivo
		fields = ['ciaconsecutivo_id', 'cia_id', 'tipo_documento', 'numero']

class CiaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cia
		fields = ['cia_id', 'razon_social', 'rif']

class UserCiaSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserCia
		fields = ['user_cia_id', 'cia', 'tipo_usuario']

class UserLogSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserLog
		fields = ['user_log_id', 'cia', 'fecha', 'sesion']

# class PersonaSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Persona
# 		# fields = ('__all__')  
# 		fields = ('persona_id', 'cia', 'nombre', 'apellido','cedula_rif', 'juridica', 'activo', 'bloqueado', 'ultima_operacion', 'email')

class PersonaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Persona
		fields = ['persona_id', 'cia', 'nombre', 'apellido','cedula_rif', 'juridica', 'activo', 'bloqueado', 'ultima_operacion', 'email']

class PersonaCortoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Persona
		fields = ['nombre', 'apellido','cedula_rif', 'juridica', 'activo', 'bloqueado']


class PersonaJuridicaSerializer(serializers.ModelSerializer):
	class Meta:
		model = PersonaJuridica
		fields = ['persona', 'registro_mercantil', 'nro_registro', 'tomo', 'fecha_registro']

class PersonaNaturalSerializer(serializers.ModelSerializer):
	class Meta:
		model = PersonaNatural
		fields = ['persona', 'razon_social', 'rif', 'fecha_nacimiento', 'sexo', 'estado_civil']

class ProductoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Producto
		fields = ('producto_id', 'cia', 'codigo', 'descripcion', 'precio', 'costo', 'existencia', 'observaciones')

class DireccionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Direccion
		fields = ['direccion_id', 'persona', 'ciudad', 'estado', 'pais', 'direccion', 'direccion_completa']

class SesionTrabajoSerializer(serializers.ModelSerializer):
	class Meta:
		model = SesionTrabajo
		fields = ['sesion_id', 'mitoken', 'cia', 'parametros']

class DocRepSerializer(serializers.ModelSerializer):	
	persona = PersonaCortoSerializer(many=False,read_only=True)
	ucrea = UsuarioSerializer(many=False,read_only=True)
	class Meta:
		model = DocRep		    
		fields = ['docrep_id', 'cia', 'persona', 'direccion', 'ucrea', 'origen', 'tipo_documento', 'numero', 'credito', 'dias_credito', 'fecha_emision', 'fecha_vencimiento', 'fecha_anulacion', 'subtotal', 'impuesto', 'total', 'observaciones']

class DocRepDetSerializer(serializers.ModelSerializer):
	class Meta:
		model = DocRepDet
		fields = ['docrepdet_id', 'docrep', 'producto', 'cantidad', 'precio', 'costo']

# fields = ('__all__') 
# persona = PersonaSerializer(many=False, read_only=True)
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

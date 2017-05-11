from django.contrib import admin

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


from ia.models import Pais, Estado, Ciudad, Usuario
from ia.models import Cia, UserCia, UserLog, Persona, PersonaJuridica, PersonaNatural
from ia.models import Producto, Direccion, SesionTrabajo, DocRep, DocRepDet, CiaConsecutivo

# Register your models here.

# ////////////////////////////////////////////////////////////////////////////////////////////
#  Definicion del Usuario
# ////////////////////////////////////////////////////////////////////////////////////////////

class UserCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:			
		model = Usuario
		fields = ('email', 'name', 'is_active', 'nombre', 'apellido', 'tipo',  'fecha_nacimiento')

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = Usuario

		fields = ('email', 'name', 'is_active', 'nombre', 'apellido', 'tipo', 'fecha_nacimiento')
		# fields = ('email', 'password', 'date_of_birth', 'is_active', 'is_admin')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]


class UserAdmin(BaseUserAdmin):
	# The forms to add and change user instances
	form = UserChangeForm
	add_form = UserCreationForm

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ('email', 'fecha_nacimiento', 'is_staff')
	list_filter = ('is_staff',)
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {'fields': ('fecha_nacimiento',)}),
		('Permissions', {'fields': ('is_staff',)}),
	)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'fecha_nacimiento', 'password1', 'password2')}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(Usuario, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

# ////////////////////////////////////////////////////////////////////////////////////////////


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
	list_display = ('pais_id', 'nombre', 'codigo')

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
	list_display = ('pais_id', 'estado_id', 'nombre', 'codigo', 'fecha', 'costo', 'activo')

@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
	list_display = ('estado_id', 'ciudad_id', 'nombre', 'codigo')

# @admin.register(UserExtension)
# class UserExtensionAdmin(admin.ModelAdmin):
# 	list_display = ('usuario', 'tipo', 'bloqueado', 'genero_codigo', 'codigo_gen', 'fecha_gen', 'birth_date')

@admin.register(Cia)
class CiaAdmin(admin.ModelAdmin):
	list_display = ('cia_id', 'razon_social', 'rif')

@admin.register(CiaConsecutivo)
class CiaConsecutivoAdmin(admin.ModelAdmin):
	list_display = ('ciaconsecutivo_id', 'cia_id', 'tipo_documento', 'numero')

@admin.register(UserCia)
class UserCiaAdmin(admin.ModelAdmin):
	list_display = ('user_cia_id', 'cia', 'tipo_usuario')

@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
	list_display = ('user_log_id', 'cia', 'fecha', 'sesion')

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
	list_display = ('persona_id', 'cia', 'nombre', 'apellido','cedula_rif', 'juridica', 'activo', 'bloqueado', 'ultima_operacion', 'email')

@admin.register(PersonaJuridica)
class PersonaJuridicaAdmin(admin.ModelAdmin):
	list_display = ('persona', 'registro_mercantil', 'nro_registro', 'tomo', 'fecha_registro')

@admin.register(PersonaNatural)
class PersonaNaturalAdmin(admin.ModelAdmin):
	list_display = ('persona', 'razon_social', 'rif', 'fecha_nacimiento', 'sexo', 'estado_civil')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
	list_display = ('producto_id', 'cia', 'codigo', 'descripcion', 'precio', 'costo', 'existencia', 'observaciones')

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
	list_display = ('direccion_id', 'persona', 'ciudad', 'estado', 'pais', 'direccion', 'direccion_completa')

@admin.register(SesionTrabajo)
class SesionTrabajoAdmin(admin.ModelAdmin):
	list_display = ('sesion_id', 'mitoken', 'cia', 'parametros')

@admin.register(DocRep)
class DocRepAdmin(admin.ModelAdmin):
	list_display = ('docrep_id', 'cia', 'persona', 'direccion', 'origen', 'tipo_documento', 'numero', 'credito', 'dias_credito', 'fecha_emision', 'fecha_vencimiento', 'fecha_anulacion', 'subtotal', 'impuesto', 'total', 'observaciones')

@admin.register(DocRepDet)
class DocRepDetAdmin(admin.ModelAdmin):
	list_display = ('docrepdet_id', 'docrep', 'producto', 'cantidad', 'precio', 'costo')



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
from django.contrib import admin
from .models import CustomUser,objeto,SolicitudPrestamo
# Register your models here.

@admin.register(CustomUser)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'fecha_creacion') 
    search_fields = ('nombre', 'correo')
#admin.site.register(Usuario, UsuarioAdmin)
@admin.register(objeto)
class objetoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'imagen', 'imagen2','imagen3','propietario')  # Ajusta los campos según tu modelo
    list_filter = ('nombre',)
    search_fields = ('nombre', 'propietario')  # Habilita búsqueda

@admin.register(SolicitudPrestamo)
class solicitudAdmin(admin.ModelAdmin):
    list_display = ('objeto', 'solicitante', 'propietario', 'mensaje')  # Ajusta los campos según tu modelo
    list_filter = ('objeto',)



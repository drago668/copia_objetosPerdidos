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
    list_display = ('id','nombre', 'descripcion', 'imagen', 'imagen2','imagen3','propietario')  # Ajusta los campos según tu modelo
    list_filter = ('id','nombre',)
    search_fields = ('id','nombre', 'propietario')  # Habilita búsqueda
    ordering = ('id',)

@admin.register(SolicitudPrestamo)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'objeto_principal', 'objeto_secundario', 'solicitante', 'propietario', 'mensaje','estado')
    list_filter = ('objeto_principal', 'propietario')  # Filtro adicional por propietario
    search_fields = ('objeto_principal__nombre', 'solicitante__nombre', 'mensaje','estado')  # Búsqueda más detallada
    ordering = ('id',)


from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Usuario,Rol,Trabajadores,Sucursal,Empresa


admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Permission)
admin.site.register(ContentType)
admin.site.register(Trabajadores)
admin.site.register(Sucursal)
admin.site.register(Empresa)
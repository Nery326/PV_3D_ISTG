from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType



class Rol(models.Model):
    """Model definition for Rol."""

    # TODO: Define fields here
    id = models.AutoField(primary_key=True)
    rol = models.CharField('Rol', max_length=50, unique=True)

    class Meta:
        """Meta definition for Rol."""

        verbose_name = 'Rol'
        verbose_name_plural = 'Rols'

    def __str__(self):
        """Unicode representation of Rol."""
        return self.rol

    def save(self, *args, **kwargs):
        permisos_defecto = ['add', 'change', 'delete', 'view']
        if not self.id:
            nuevo_grupo, creado = Group.objects.get_or_create(name=f'{self.rol}')
            for permiso_temp in permisos_defecto:
                permiso, created = Permission.objects.update_or_create(
                    name=f'Can {permiso_temp} {self.rol}',
                    content_type=ContentType.objects.get_for_model(Rol),
                    codename=f'{permiso_temp}_{self.rol}'
                )
                if creado:
                    nuevo_grupo.permissions.add(permiso.id)
            super().save(*args, **kwargs)
        else:
            rol_antiguo = Rol.objects.filter(id=self.id).values('rol').first()
            if rol_antiguo['rol'] == self.rol:
                super().save(*args, **kwargs)
            else:
                Group.objects.filter(name=rol_antiguo['rol']).update(name=f'{self.rol}')
                for permiso_temp in permisos_defecto:
                    Permission.objects.filter(codename=f"{permiso_temp}_{rol_antiguo['rol']}").update(
                        codename=f'{permiso_temp}_{self.rol}',
                        name=f'Can {permiso_temp} {self.rol}'
                    )
                super().save(*args, **kwargs)

class Sucursal(models.Model):
    sucursal = models.CharField(max_length=15)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    correo = models.CharField(max_length=50)
    imagen = models.ImageField('Imagen de Sucursal', upload_to='sucursal/', max_length=200, blank=True, null=True)
    estado= models.BooleanField('Estado', default= True)

    def sucursales(self):
        return "{} ".format(self.sucursal)
    def __str__(self):
        return self.sucursales()
    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        db_table = 'Sucursal'

class Trabajadores(models.Model):
    ci = models.CharField(max_length=10)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    correo = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    estadoCivil = models.CharField(max_length=10,null=True)
    nacionalidad = models.CharField(max_length=50,null=True)
    estado= models.BooleanField('Estado', default= True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, blank=True, null=True)


    def Trabajadores(self):
        return "{} {} ".format(self.nombre, self.apellido)
    def __str__(self):
        return self.Trabajadores()

    class Meta:
        verbose_name = 'Trabajadore'
        verbose_name_plural = 'Trabajadores'
        db_table = 'Trabajadores'

class UsuarioManager(BaseUserManager):
    def _create_user(self, username, email, nombres, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            nombres=nombres,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, nombres, is_staff, password=None, **extra_fields):
        return self._create_user(username, email, nombres, password, is_staff, False, **extra_fields)

    def create_superuser(self, username, email, nombres, password=None, **extra_fields):
        return self._create_user(username, email, nombres, password, True, True, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Nombre de usuario', unique=True, max_length=100, null=True)
    email = models.EmailField('Correo Electrónico', max_length=254, unique=True)
    nombres = models.CharField('Nombres', max_length=200, blank=True, null=True)
    apellidos = models.CharField('Apellidos', max_length=200, blank=True, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, blank=True, null=True)
    trabajador = models.ForeignKey(Trabajadores, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.BooleanField('Estado', default=True)
    imagen = models.ImageField('Imagen de Perfil', upload_to='perfil/', max_length=200, blank=True, null=True, default='user.png')
    sucursal = models.ForeignKey(Sucursal, null=True, blank=True, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombres']

    class Meta:
        permissions = [('permiso_desde_codigo', 'Este es un permiso creado desde código'),
                       ('segundo_permiso_codigo', 'Segundo permiso creado desde codigo')]

    def __str__(self):
        return f'{self.nombres},{self.apellidos}'

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
            if self.rol is not None:
                grupo = Group.objects.filter(name=self.rol.rol).first()
                if grupo:
                    self.groups.add(grupo)
                super().save(*args, **kwargs)
        else:
            if self.rol is not None:
                grupo_antiguo = Usuario.objects.filter(id=self.id).values('rol__rol').first()
                # print(grupo_antiguo['rol__rol'])
                # print(self.rol.rol)
                if grupo_antiguo['rol__rol'] == self.rol.rol:
                    print("Entro en igualdad de roles")
                    super().save(*args, **kwargs)
                else:
                    grupo_anterior = Group.objects.filter(name=grupo_antiguo['rol__rol']).first()
                    if grupo_anterior:
                        print(grupo_anterior)
                        self.groups.remove(grupo_anterior)
                    nuevo_grupo = Group.objects.filter(name=self.rol.rol).first()
                    if nuevo_grupo:
                        self.groups.add(nuevo_grupo)
                    super().save(*args, **kwargs)


class Empresa(models.Model):
    comercial = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=250)
    Ruc = models.CharField(max_length=13)
    estado= models.BooleanField('Estado', default= True)
    class Meta:
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'
        db_table = 'empresa'



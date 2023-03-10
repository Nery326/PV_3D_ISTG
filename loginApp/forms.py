from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario
from .models import Trabajadores
from django.forms import widgets


class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


class FormularioUsuario(forms.ModelForm):
    """ Formulario de Registro de un Usuario en la base de datos

    Variables:

        - password1:    Contraseña
        - password2:    Verificación de la contraseña

    """
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña...',
            'id': 'password1',
            'required': 'required',
        }
    ))

    password2 = forms.CharField(label='Contraseña de Confirmación', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nuevamente su contraseña...',
            'id': 'password2',
            'required': 'required',
        }
    ))

    class Meta:
        model = Usuario
        fields = ('email', 'username', 'nombres', 'apellidos', 'rol', 'trabajador', 'imagen')
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'formulario__input',
                    'placeholder': 'Correo Electrónico',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'formulario__input',
                    'placeholder': 'Ingrese su nombre',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'formulario__input',
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'formulario__input',
                    'placeholder': 'Ingrese su nombre de usuario',
                }
            ),
            'rol': forms.Select(
                attrs={
                    'class': 'formulario__input'
                }
            ),
            'trabajador': forms.Select(
                attrs={
                    'class': 'formulario__input'
                }
            )
        }

    def clean_password2(self):
        """ Validación de Contraseña

        Metodo que valida que ambas contraseñas ingresadas sean igual, esto antes de ser encriptadas
        y guardadas en la base dedatos, Retornar la contraseña Válida.

        Excepciones:
        - ValidationError -- cuando las contraseñas no son iguales muestra un mensaje de error
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden!')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CambiarPasswordForm(forms.Form):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su nueva contraseña...',
            'id': 'password1',
            'required': 'required',
        }
    ))

    password2 = forms.CharField(label='Contraseña de Confirmación', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nuevamente la nueva contraseña...',
            'id': 'password2',
            'required': 'required',
        }
    ))

    def clean_password2(self):
        """ Validación de Contraseña

        Metodo que valida que ambas contraseñas ingresadas sean igual, esto antes de ser encriptadas
        y guardadas en la base dedatos, Retornar la contraseña Válida.

        Excepciones:
        - ValidationError -- cuando las contraseñas no son iguales muestra un mensaje de error
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden!')
        return password2

class TrabajadoresForm(forms.ModelForm):
    class Meta:
        model = Trabajadores
        fields = '__all__'
        widgets = {
            'ci': forms.TextInput(
                attrs={
                    'class': 'formulario__input',
                    'placeholder': '0905020810',
                    'id': 'cedula',
                    'name': 'cedula',
                }
            ),
            'nombre': forms.TextInput(
                attrs= {
                    'class':'formulario__input',
                    'placeholder': 'John Doe',
                    'id': 'nombre',
                    'name': 'nombre',
                }
            ),
            'apellido': forms.TextInput(
                attrs={
                    'class': 'formulario__input',
                    'placeholder': 'Peréz',
                    'id': 'apellido',
                    'name': 'apellido',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'formulario__input',
                    'placeholder': 'Guayaquil',
                    'id': 'direccion',
                    'name': 'direccion',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'formulario__input',
                    'placeholder': '0958933521',
                    'id': 'telefono',
                    'name': 'telefono',
                }
            ),
            'correo': forms.TextInput(
                attrs={
                    'class': 'formulario__input',
                    'placeholder': 'example@hotmail.com',
                    'id': 'correo',
                    'name': 'correo',
                }
            ),
            'nacionalidad': forms.TextInput(
                attrs={
                    'class': 'formulario__input',
                    'placeholder': 'Ecuatoriano',
                    'id': 'nacionalidad',
                    'name': 'nacionalidad',
                }
            ),
            'estadoCivil': forms.TextInput(
                attrs={
                    'class': 'formulario__input',
                    'placeholder': 'Soltero',
                    'id': 'estado',
                    'name': 'estado',
                }
            ),
            'estado': forms.CheckboxInput(
                attrs={
                    'class': 'formulario__checkbox',
                    'id': 'terminos',
                    'name': 'terminos',
                }
            ),
        }
import json
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.serializers import serialize
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import Http404
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from .mixins import LoginYSuperStaffMixin, ValidarPermisosMixinUsuario, LoginMixin
from .models import Trabajadores, Usuario
from .forms import (FormularioLogin, FormularioUsuario, CambiarPasswordForm,TrabajadoresForm
)
class Inicio(LoginRequiredMixin,TemplateView):
    """Clase que renderiza el index del sistema"""
    template_name = 'menu.html'
    groups_required = ['Grupo1', 'Grupo2']

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)


def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


class CrearTrabajador(LoginYSuperStaffMixin,ValidarPermisosMixinUsuario,CreateView):
    permission_required = ('loginApp.view_Trabajadore', 'loginApp.Trabajadore',
                           'loginApp.delete_Trabajadore', 'loginApp.change_Trabajadore')
    model = Trabajadores
    form_class = TrabajadoresForm
    template_name = 'crearTrabajador.html'
    success_url = reverse_lazy('listado_trabajadores')

class listTrabajadores(LoginYSuperStaffMixin,ValidarPermisosMixinUsuario,ListView):
    permission_required = ('loginApp.view_Trabajadore', 'loginApp.Trabajadore',
                           'loginApp.delete_Trabajadore', 'loginApp.change_Trabajadore')
    model = Trabajadores
    template_name = 'listarTrabajadores.html'
    queryset = Trabajadores.objects.filter(estado=True)

class EditarTrabajador(LoginYSuperStaffMixin,ValidarPermisosMixinUsuario,UpdateView):
    permission_required = ('loginApp.view_Trabajadore', 'loginApp.Trabajadore',
                           'loginApp.delete_Trabajadore', 'loginApp.change_Trabajadore')
    model = Trabajadores
    template_name = 'editarTrabajador.html'
    form_class = TrabajadoresForm
    success_url = reverse_lazy('listado_trabajadores')


class EliminarTrabajador(LoginYSuperStaffMixin,ValidarPermisosMixinUsuario,DeleteView):
    permission_required = ('loginApp.view_Trabajadore', 'loginApp.Trabajadore',
                           'loginApp.delete_Trabajadore', 'loginApp.change_Trabajadore')
    model = Trabajadores
    template_name = 'trabajadores_confirm_delete.html'


    def post(self, request, pk, *args, **kwargs):
        object = Trabajadores.objects.get(id=pk)
        object.estado = False
        object.save()
        return redirect('listado_trabajadores')

class listUsuarios(LoginYSuperStaffMixin,ValidarPermisosMixinUsuario,ListView):
    permission_required = ('loginApp.view_usuario', 'loginApp.add_usuario',
                           'loginApp.delete_usuario', 'loginApp.change_usuario')
    model = Usuario
    template_name= 'listaUsuarios.html'


class RegistarUsuario(LoginYSuperStaffMixin,ValidarPermisosMixinUsuario,CreateView):
    permission_required = ('loginApp.view_usuario', 'loginApp.add_usuario',
                           'loginApp.delete_usuario', 'loginApp.change_usuario')
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'crearUsuario.html'


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            nuevo_usuario = Usuario(
                email = form.cleaned_data.get('email'),
                username = form.cleaned_data.get('username'),
                nombres=form.cleaned_data.get('nombres'),
                apellidos=form.cleaned_data.get('apellidos'),
                rol=form.cleaned_data.get('rol'),
                trabajador=form.cleaned_data.get('trabajador'),
                imagen=form.cleaned_data.get('imagen'),

            )
            nuevo_usuario.set_password(form.cleaned_data.get('password1'))
            nuevo_usuario.save()
            return redirect('listaUsuarios')
        else:
            return render(request,self.template_name,{'form': form})

class CambiarPassword(LoginMixin, View):
    template_name = 'cambiar_password.html'
    form_class = CambiarPasswordForm
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = Usuario.objects.filter(id=request.user.id)
            if user.exists():
                user = user.first()
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                logout(request)
                return redirect(self.success_url)
            return redirect(self.success_url)
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form': form})
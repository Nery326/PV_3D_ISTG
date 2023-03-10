from django.shortcuts import render, redirect
from .models import MenuList, mainmenu
from .serializers import menuserializer, submenuserializer
from django.db.models import Avg, Count, Min, Sum
from loginApp.models import Usuario,Trabajadores



# Create your views here.
def dynamicmenu(request):
    try:
        menuList = MenuList.menulist_objects.values('menuname').order_by('MenuType').annotate(Count('menuname'))
        submenuList = MenuList.menulist_objects.all().filter(id__in=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29])
        mainmenu = menuserializer(menuList, many=True)
        data = mainmenu.data
        # print(data)
        request.session['mainM'] = data

        submenudata = submenuserializer(submenuList, many=True)
        subdata = submenudata.data
        request.session['submenu'] = subdata
        return render(request, 'menu.html', {})

    except Exception as identifier:
        return render(request, 'menu.html', {})

def dashobord(request):
    trabajador = Trabajadores.objects.filter(estado=True)
    usuario = Usuario.objects.filter()
    total_trabjadores = trabajador.count()
    total_usuarios = usuario.count()
    context = {
        'total_trabjadores': total_trabjadores,
        'total_usuarios': total_usuarios,
    }
    return render(request, 'dashboard.html', context)
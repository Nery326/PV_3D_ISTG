from django.db import models
# Create your models here.

class mainmenu(models.Model):
    menucode = models.IntegerField()
    menuname = models.CharField(max_length=100)
    menutype = models.IntegerField()

    def __str__(self):
        return self.menuname

    mainmenulist_objects = models.Manager()


class MenuList(models.Model):
    Menucode = models.IntegerField()
    MenuType = models.IntegerField()
    menuname = models.CharField(max_length=100)
    submenuname = models.CharField(max_length=100)
    menulink = models.CharField(max_length=100)
    iconlink = models.CharField(max_length=100, null=True)
    menu = models.ForeignKey(mainmenu,null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.menuname

    menulist_objects = models.Manager()
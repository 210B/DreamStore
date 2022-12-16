from django.contrib import admin
from .models import Distributor, Theme, Producer, Dream, CEO

# Register your models here.


admin.site.register(Dream)


admin.site.register(CEO)


admin.site.register(Distributor)


class ProducerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}


admin.site.register(Producer, ProducerAdmin)


class ThemeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}


admin.site.register(Theme)

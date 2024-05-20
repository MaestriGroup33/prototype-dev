# Register your models here.
from django.contrib import admin

from .models import GlobalSettings
from .models import Indicators

admin.site.register(GlobalSettings)
admin.site.register(Indicators)

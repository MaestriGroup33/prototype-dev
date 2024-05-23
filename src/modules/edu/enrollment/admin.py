# Register your models here.
from django.contrib import admin

from .models import Classifications, Profile, Clients, Enrollments

admin.site.register(Profile)
admin.site.register(Clients)
admin.site.register(Classifications)
admin.site.register(Enrollments)

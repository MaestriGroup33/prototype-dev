from django.contrib import admin

from .models import Address
from .models import Graduation
from .models import HighSchool
from .models import PostGraduation
from .models import Profile

# admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(HighSchool)
admin.site.register(Graduation)
admin.site.register(PostGraduation)


# como adicionar o Address aqui ?


# Register your models here.

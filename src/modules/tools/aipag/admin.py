from django.contrib import admin

from .models import Destination
from .models import FixedInformation
from .models import Logo
from .models import PageTemplate
from .models import Script
from .models import Style
from .models import Version

admin.site.register(PageTemplate)
admin.site.register(Destination)
admin.site.register(FixedInformation)
admin.site.register(Logo)
admin.site.register(Version)
admin.site.register(Style)
admin.site.register(Script)

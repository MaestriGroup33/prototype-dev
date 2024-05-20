from django.contrib import admin

from src.modules.edu.campaigns.models import Card
from src.modules.edu.campaigns.models import Faq
from src.modules.edu.campaigns.models import LandingPage
from src.modules.edu.campaigns.models import Section
from src.modules.edu.campaigns.models import Statistic
from src.modules.edu.campaigns.models import Testimonial
from src.modules.edu.campaigns.models import ValueProposition

admin.site.register(LandingPage)
admin.site.register(Section)
admin.site.register(Card)
admin.site.register(Statistic)
admin.site.register(Testimonial)
admin.site.register(ValueProposition)
admin.site.register(Faq)


# Register your models here.

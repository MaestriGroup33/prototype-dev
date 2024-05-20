from django.urls import include
from django.urls import path

urlpatterns = [
    path("campaigns/", include("src.modules.edu.campaigns.urls")),
    path("courses/", include("src.modules.edu.courses.urls")),
    # path("charges", include("src.modules.edu.charges.urls")),
    path("enrollments/", include("src.modules.edu.enrollment.urls")),
]
# TODO: Descomente as urls para serem incluidas

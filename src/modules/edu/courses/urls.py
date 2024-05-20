from django.urls import path

from . import views

app_name = "edu.courses"
urlpatterns = [
    path(
        "details",
        view=views.CourseDetailView.as_view(),
    ),
    path(
        "all",
        view=views.CourseListView.as_view(),
    ),
    path(
        "",
        view=views.get_courses,
    ),
]

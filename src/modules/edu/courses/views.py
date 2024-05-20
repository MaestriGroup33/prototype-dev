# Create your views here.
from django.views.generic import DetailView
from django.views.generic import ListView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Course
from .serializers import CourseSerializer


class CourseListView(ListView):
    model = Course
    template_name = "edu/courses/list.html"
    context_object_name = "courses"
    paginate_by = 6


class CourseDetailView(DetailView):
    model = Course
    template_name = "edu/courses/detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = Course.objects.all()
        return context


class CourseSearchView(ListView):
    model = Course
    template_name = "edu/courses/search.html"
    context_object_name = "courses"
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Course.objects.filter(name__icontains=query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q")
        return context


class CourseReviewView(DetailView):
    model = Course
    template_name = "edu/courses/review.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = Course.objects.all()
        return context


@extend_schema(request=None, responses=None)
@api_view(["GET"])
def get_courses(request):
    courses = Course.objects.all()

    json = CourseSerializer(courses, many=True)

    return Response(json.data)

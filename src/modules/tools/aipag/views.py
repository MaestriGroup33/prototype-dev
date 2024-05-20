from django.shortcuts import render

# Create your views here.


def maestri_group_site(request):
    return render(request, "group.html")

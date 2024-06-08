# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
from django.urls import path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.decorators import login_required
from src.modules.app import views as app_views

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path(
        "home/",
        TemplateView.as_view(template_name="pages/home.html"),
    ),
    path(
        "login/",
        TemplateView.as_view(template_name="pages/login.html"),
    ),
    path(
        "register/",
        TemplateView.as_view(template_name="pages/register.html"),
    ),
    path(
        "politica/",
        TemplateView.as_view(template_name="pages/politica.html"),
    ),
    path(
        "promoters/",
        TemplateView.as_view(template_name="promoters/home.html"),
    ),
    path(
        "app/",
        include(
            [
                path(
                    "",
                    login_required(TemplateView.as_view(template_name="app/main.html")),
                    name="app_main",
                ),
                path(
                    "home/",
                    TemplateView.as_view(template_name="app/home.html"),
                    name="home",
                ),
                # path(
                #     "finance/",
                #     TemplateView.as_view(template_name="app/finances.html"),
                #     name="finance",
                # ),
                path(
                    "add-student/",
                    TemplateView.as_view(template_name="app/add_student.html"),
                    name="add_student",
                ),
                path(
                    "students/",
                    TemplateView.as_view(template_name="app/students.html"),
                    name="students",
                ),
                path(
                    "chat/",
                    TemplateView.as_view(template_name="app/chat.html"),
                    name="chat",
                ),
                path(
                    "profile/",
                    TemplateView.as_view(template_name="app/profile.html"),
                    name="profile",
                ),
                path(
                    "add-promoter/",
                    TemplateView.as_view(template_name="app/add_promoter.html"),
                    name="add_promoter",
                ),
                path(
                    "edit-promo-code/",
                    app_views.edit_promo,
                    name="edit_promo_code",
                ),
                path("finance", app_views.finances, name="finance"),
                # path("registration_form/", TemplateView.as_view(template_name="app/registration_form.html"), name="registration_form"),
                # path("registration_form_2/", TemplateView.as_view(template_name="app/registration_form_2.html"), name="registration_form_2"),
                path(
                    "codename/",
                    TemplateView.as_view(template_name="app/codename.html"),
                    name="codename",
                ),
            ]
        ),
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("src.users.urls", namespace="users")),
    path("auth/", include("src.users.authentication.urls", namespace="auth")),
    path("accounts/", include("allauth.urls")),
    path("", include("src.modules.urls")),
    # Your stuff: custom urls includes go here
    # ...
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("api/auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

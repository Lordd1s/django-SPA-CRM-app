from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions, authentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="HTTP API",
        default_version="v1",
        description="Документация приложении!",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="uaudias@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("grappelli/", include("grappelli.urls")),
    path("admin/", admin.site.urls),
    path("", include("final_course.urls")),
    path("api/auth", include("rest_framework.urls")),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # re_path(r"^.*", TemplateView.as_view(template_name="your_spa_app/index.html")),
]

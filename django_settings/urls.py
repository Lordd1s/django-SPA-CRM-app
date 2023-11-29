from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path("grappelli/", include("grappelli.urls")),
    path("admin/", admin.site.urls),
    path("", include("final_course.urls")),
    path("api/auth", include("rest_framework.urls")),
    # re_path(r"^.*", TemplateView.as_view(template_name="your_spa_app/index.html")),
]

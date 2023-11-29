from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django_settings import settings
from final_course import views

urlpatterns = [
    path("", views.home, name="home"),
    # Token
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Auth/Registrate
    path("registrate/", views.register),
    path("login/<str:pk>", views.login_user),
    # Other
    path("vacancy/", views.vacancy),
    path("cud_vacancy/<str:pk>", views.create_vacancy),
    path("cv/<str:pk>", views.cv),
    path("all_cv/", views.all_cv),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django_settings import settings
from final_course import views, async_views

urlpatterns = [
    path("", views.home, name="home"),
    # Token Authentication
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Registrate/parse username
    path("registrate/", views.register),
    path("login/<str:pk>/", views.login_user),
    # CV and CV operations
    path("vacancy/", views.vacancy),
    path("cud_vacancy/<str:pk>/", views.create_vacancy),
    path("cv/<str:pk>/", views.cv),
    path("all_cv_boss/", views.all_cv_boss),
    path("all_cv/", views.all_cv),
    path("cv_rate_get/<str:pk>/", views.like_dislike_cv_get),
    path("cv_rate_post/<str:pk>/<str:st>/", views.like_dislike_cv_post),
    # newsletter
    path("newsletter/", views.news_to_front),
    # download xlsx
    path("download_xlsx/period/<str:period>", views.download_xlsx_period),
    path("download_xlsx/custom", views.download_xlsx_custom),
    # list of goods / services
    path("applications/solution", views.applications),  # bosses
    path("application/", views.application),  # masters
    # profile
    path("profile/", views.profile),
    # chat
    path("chat_groups/", async_views.groups),  # Список подписанных групп
    path("chat/", async_views.group),  # Сама группа
    path("create_group/", async_views.create_group),  # Создание группы
]


# websocket
websocket_urlpatterns = [
    path("ws/<slug:group_name>/", async_views.GroupChatConsumer.as_asgi())
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

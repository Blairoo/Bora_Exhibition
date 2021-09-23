from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.main),
    path('join', views.join),
    path('login', views.login),
    path("logout", views.logout),
    path('checkid', views.checkid),
    path("exhibition", views.exhibition, name="exhibition"),
    path('up', views.upload_file),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
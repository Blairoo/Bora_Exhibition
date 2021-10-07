from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('', views.main),
    # path('join', views.join),
    # path('login', views.login),
    # path("logout", views.logout),
    # path('checkid', views.checkid),
    # path("exhibition", views.exhibition, name="exhibition"),
    # path('up', views.upload_file),
    path('main', views.main, name="main"),
    path('checkid', views.checkid),
    path('signup', views.signup, name="signup"),
    path('ajaxlogin', views.ajaxlogin, name="ajaxlogin"),
    path('logout', views.logout, name="logout"),
    path('edit', views.edit, name="edit"),
    path('withdrawal', views.withdrawal, name="withdrawal"),
    path("exhibition", views.list, name="list"),
    path('exhibition/<str:pk>', views.detail, name='detail'),
    path('ajaxreserve', views.ajaxreserve, name='ajaxreserve'),
    path('delete_res', views.delete_res, name="delete_res"),
    path('ajaxleave_rev', views.ajaxleave_rev, name="ajaxleave_rev"),
    path('ajaxdelete_rev', views.ajaxdelete_rev, name="ajaxdelete_rev"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
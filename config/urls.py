from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from catalog import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("jogo/<int:pk>/", views.detalhe_jogo, name="detalhe_jogo"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/adicionar/", views.adicionar_jogo, name="adicionar_jogo"),
    path("dashboard/editar/<int:pk>/", views.editar_jogo, name="editar_jogo"),
    path("dashboard/apagar/<int:pk>/", views.apagar_jogo, name="apagar_jogo"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

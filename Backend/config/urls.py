"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.infra.auth.views.login_views import LoginApiView
from apps.infra.auth.views.register_views import RegisterUserAPIView
from django.urls import path
from apps.infra.auth.views.generate_invite_view import GenerateInviteAPIView
from apps.infra.auth.views.register_views import RegisterByInviteAPIView
from apps.pesagem.views.veiculos_views import VeiculoListApiView,VeiculoCreateApiView
from apps.pesagem.views.colaborador_views import ColaboradorCreateApiView,ColaboradorListApiView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/login/", LoginApiView.as_view(), name="login"),
    path("api/register/", RegisterUserAPIView.as_view(), name="register"),
    path("api/invite/", GenerateInviteAPIView.as_view(),name="Invite"),
    path("api/register-by-invite/", RegisterByInviteAPIView.as_view(),name="InviteRegister"),
    path("api/veiculos-list/",VeiculoListApiView.as_view(),name="VeiculosList"),
    path("api/veiculo-create/",VeiculoCreateApiView.as_view(),name="VeiculoCreate"),
    path("api/create-colaborador/",ColaboradorCreateApiView.as_view(),name="ColaboradorCreate"),
    path("api/colaborador-list/",ColaboradorListApiView.as_view(),name="ColaboradorList")
]

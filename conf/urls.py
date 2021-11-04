"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import include, path

from accounts.views import SignUpView
from operations import views as operations_views


API_VERSION = "v1"


urlpatterns = [
    path("", operations_views.InitialPageListView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("operacoes/", include("operations.urls", namespace="operations")),
    path("usuario/", include("users.urls", namespace="users")),
    path(f"{API_VERSION}/dados/", include("coredata.api_urls", namespace="coredata")),
    path(f"{API_VERSION}/operacoes/", include("operations.api_urls", namespace="api-operations")),
]

# Auth views
urlpatterns += [
    path("conta/login", auth_views.LoginView.as_view(), name="login"),
    path("conta/logout", auth_views.LogoutView.as_view(), name="logout"),
    path("conta/mudar-senha", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("conta/mudar-senha/feito", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("conta/redefinir-senha", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("conta/redefinir-senha/enviado", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("conta/nova-senha/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})",
         auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("conta/nova-senha/pronto", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("conta/cadastro", SignUpView.as_view(), name="signup"),
]

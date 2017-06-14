"""chat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from chatApp.admin_panel import get_all_users, add_user_to_black_list, remove_user_from_black_list
from chatApp.views import Registration, LoginController, ChatController, AdminController, BanController

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$',TemplateView.as_view(template_name="index.html")),
    url(r'^registration$',Registration.as_view()),
    url(r'^login$', LoginController.as_view()),
    url(r'^chat$', ChatController.as_view()),
    url(r'^get_users$', get_all_users),
    url(r'^add$', add_user_to_black_list),
    url(r'^remove/([\w]+)$', remove_user_from_black_list),
    url(r'^admin_panel$', AdminController.as_view()),
    url(r'^ban$', BanController.as_view()),

]

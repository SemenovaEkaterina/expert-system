"""expert URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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

# from django.contrib import admin
from expert_app.views import Home, Login, Signup, Logout, OfficeDashboard, OfficeSystems

urlpatterns = [
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^signup/$', Signup.as_view(), name='signup'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^office/systems/(?P<page>\w*)?$', OfficeSystems.as_view(), name='office_systems'),
    url(r'^office/', OfficeDashboard.as_view(), name='office'),
    url(r'^$', Home.as_view(), name='home'),
]

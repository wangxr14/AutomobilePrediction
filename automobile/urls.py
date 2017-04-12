"""automobile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin

from . import view

urlpatterns = [
    url(r'^$', view.login),
	url(r'^loginWithFace/$',view.loginWithFace),
	url(r'^sign_up/$',view.signUp),
	url(r'^search_page/$',view.renderSearchPage),
	url(r'^result/$',view.renderResult),
]

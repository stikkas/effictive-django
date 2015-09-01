"""addressbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
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
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
import contacts.views

admin.autodiscover()

urlpatterns = [
    url(r'^$', contacts.views.ListContactView.as_view(), name='contacts-list'),
    url(r'^new/$', contacts.views.CreateContactView.as_view(),
        name='contacts-new'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^edit/(?P<pk>\d+)/addresses/$', contacts.views.EditContactAddressView.as_view(),
        name='contacts-edit-addresses'),
    url(r'^edit/(?P<pk>\d+)/$', contacts.views.UpdateContactView.as_view(),
        name='contacts-edit'),
    url(r'^delete/(?P<pk>\d+)/$', contacts.views.DeleteContactView.as_view(),
        name='contacts-delete'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^(?P<pk>\d+)/$', contacts.views.DetailContactView.as_view(),
        name='contacts-view'),
    url(r'^(?P<name>\w+)/$', contacts.views.ListContactByNameView.as_view(),
        name='contacts-by_name-list'),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()


from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
        url(r'^dashboard$', views.dashboard),
         url(r'^login$', views.login),
         url(r'^register$', views.register),
         url(r'^new_item$', views.new_item),
         url(r'^create$', views.create),
         url(r'^lists/(?P<id>\d+)$', views.lists),
         url(r'^add/(?P<id>\d+)$', views.add),
         url(r'^remove/(?P<id>\d+)$', views.remove),
         url(r'^destroy/(?P<id>\d+)$', views.destroy),
         url(r'^logout$', views.logout)
]

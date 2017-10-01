from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^friends/$', views.index, name = "all_friends"),
    url(r'^add/(?P<id>\d+)$', views.add, name = "add_friend"),
    url(r'^remove/(?P<id>\d+)$', views.remove, name = "remove_friend"),
    url(r'^user/(?P<id>\d+)$', views.user, name = "user_page"),
]

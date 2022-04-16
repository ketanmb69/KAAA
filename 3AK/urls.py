from django.contrib import admin
from django.conf.urls import include,url
from django.urls import include, path
from rest_framework import routers

from . import views
from .views import AccountViews

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
#outer.register(r'roles', views.RoleViewSet)

urlpatterns = [
    url(r'^',include('server.urls',namespace="server")),
    url(r'^admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('views/', AccountViews.as_view()),
    path('views/<int:id>', AccountViews.as_view())
]

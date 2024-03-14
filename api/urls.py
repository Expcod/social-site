from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'my-model', views.MyModelView, basename='MyModel')


urlpatterns = [
    path('router/', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    # path('', views.list_data)
]
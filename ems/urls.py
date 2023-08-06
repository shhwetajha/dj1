from django.urls import path,include
from ems.views import *
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('viewapi',viewset_func,basename='viewapi')



urlpatterns=[
    path('api/',view_func),
    path('api/<int:pk>/',view_func),
    path('apic/',getAPI.as_view()),
    path('apic/<int:pk>/',getAPI.as_view()),
    path('',include(router.urls)),
    path('home/<int:id>/',home)
]
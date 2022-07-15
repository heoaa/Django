from django.urls import path
from . import views

urlpatterns = [
    path('show2/', views.show2),
    path('oneshow/', views.oneshow),
    path('insert/', views.insert),
    path('main/', views.main),
    path('lprod_list/', views.view_Lprod_List),
    path('lprod/', views.view_Lprod),
]

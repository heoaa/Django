from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test),
    path('createTable/', views.createTable),
    path('insertTest/', views.set_Survey_Insert_test),
    path('list/', views.view_Survey_List),
    path('survey/', views.view_Survey),
    path('insert/', views.set_Survey_Insert),
    path('analysis/', views.survey_Analysis),
]

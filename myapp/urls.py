from django.urls import path
import myapp.views as views

urlpatterns = [
    path('getProbability', views.getProbability),
    path('getSymptoms', views.getSymptoms),
]
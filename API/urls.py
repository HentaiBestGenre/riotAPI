from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('summoner/<str:region>/<str:s_name>', views.summoner, name='summoner'),
    path('match/<str:match_id>', views.match, name='match'),
]

app_name = 'API'

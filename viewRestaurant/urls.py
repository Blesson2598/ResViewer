from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('show', views.show,name='show'),
    path('showres', views.showres,name='showres'),
    path('showkey/<int:show_key>/',views.showkey),
]
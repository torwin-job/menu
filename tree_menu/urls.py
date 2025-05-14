from django.urls import path
from . import views

app_name = 'tree_menu'

urlpatterns = [
    path('', views.menu_example, name='menu_example'),
] 
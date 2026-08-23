from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('registerproject/',views.register_project, name='register_project')

]

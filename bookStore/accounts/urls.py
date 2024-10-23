from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register,name='register'), 
    path('userInfo/', views.current_user,name='user_info'), 
    path('userInfo/update', views.update_user,name='update_user'), 

]
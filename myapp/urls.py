from django.urls import path
from myapp import views

app_name='myapp'

urlpatterns = [
    path('register/',views.register,name="registration"),
    path('user_login/',views.user_login,name="user_login"),
]

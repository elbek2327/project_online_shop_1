from django.urls import path
from shop import views
from users import views

app_name = 'users'




urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('logout/', views.logout_page, name='logout_page')
]

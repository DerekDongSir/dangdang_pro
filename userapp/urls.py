from django.urls import path
from userapp import views
app_name = 'userapp'
urlpatterns = [
    path('register/',views.register,name='register'),
    path('check_email/',views.check_email,name='check_email'),
    path('generate_code/',views.generate_code,name='generate_code'),
    path('check_code/',views.check_code,name='check_code'),
    path('activate_user/',views.activate_user,name='activate_user'),
    path('registerlogic/',views.registerlogic,name='registerlogic'),
    path('login/',views.login,name='login'),
    path('loginlogic/',views.loginlogic,name='loginlogic'),
    path('login_jump',views.login_jump,name='login_jump'),
    path('logout/',views.logout,name='logout'),
]
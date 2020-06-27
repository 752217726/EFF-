from django.urls import path
from userapp import views
app_name='userapp'

urlpatterns=[
    path('register/',views.register,name='register'),
    path('registerlogic/',views.register_logic,name='registerlogic'),
    path('checkname/',views.check_name,name='checkname'),
    path('setimg/',views.setImage,name='setimg'),
    path('captchlogic/',views.captch_logic,name='captchlogic'),
    path('login/',views.login,name='login'),
    path('loginlogic/',views.login_logic,name='loginlogic'),
    path('home/',views.home,name='home'),
    path('forget_pwd/', views.forget_pwd, name='forget_pwd'),
    path('forgetpwdlogic/', views.forget_pwd_logic, name='forgetpwdlogic'),
    path('resetpwd/', views.reset_pwd, name='resetpwd'),
    path('resetpwdlogic/', views.reset_pwd_logic, name='resetpwdlogic'),
    path('logout/',views.logout,name='logout'),
    path('active/', views.active, name='active'),
    path('reactive/', views.reactive, name='reactive'),
]




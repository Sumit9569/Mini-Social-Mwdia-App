from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),

    # 👇 YE PEHLE AAYEGA (IMPORTANT)
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # 👇 YE BAAD ME AAYEGA
    path('profile/<str:username>/', views.profile_view, name='profile'),

    path('follow/<str:username>/', views.follow_user, name='follow_user'),
]
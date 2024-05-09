from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('start', views.start, name='begin'),
    path('voice', views.voice, name='voice'),
    path('prediction', views.prediction, name='prediction'),
    path('save_audio', views.save_audio, name='save_audio'),

    path('answer', views.answer, name='answer'),
    path('chat', views.chat, name='chat'),
    path('evaluate', views.evaluate, name='evaluate'),
    
    path('signup/validate', views.signup_validate, name='signup_validate'),
    path('login', views.c_login, name='login'),
    path('login/validate', views.login_validate, name='login_validate'),
    path('logout', views.c_logout, name='logout'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.translate_view, name='translate'),
    path('text/', views.translate_text, name='translate_text'),
    path('voice/start/', views.start_voice_chat, name='start_voice_chat'),
    path('voice/process/', views.process_voice_input, name='process_voice_input'),
    path('chat/', views.text_chat, name='text_chat'),
    path('voice/end/', views.end_voice_chat, name='end_voice_chat'),
]
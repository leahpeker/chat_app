from django.urls import path

from . import views

urlpatterns = [
        path('', views.home, name='home'),
        path('conversation/<int:pk>/', views.conversation_detail, name='conversation_detail'),
        path('conversation_search/<title>/', views.conversation_search_results, name='conversation_search_results'),
        path('message_search/<search_text>/', views.message_search_results, name='message_search_results'),
]
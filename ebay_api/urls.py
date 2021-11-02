from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ebay-challenge-and-response-verification', views.ebay_challenge_and_response_verification, name='ebay_challenge_and_response_verification'),
]

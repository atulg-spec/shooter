# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create-campaign/', views.create_campaign, name='create_campaign'),
    path("getcampaigns/<str:ipaddress>",views.getcampaigns,name='getcampaigns'),
]

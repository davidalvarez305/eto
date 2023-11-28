from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login', views.Login.as_view(), name='login'),
    path('quote', views.QuoteView.as_view(), name='quote'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('privacy-policy', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('about', views.HomeView.as_view(), name='about'),
    path('services', views.ServicesView.as_view(), name='services'),
    path('pressure-washing', views.PPCLandingPageView.as_view(), name='pressure_washing'),
    path('twillio/images', views.handle_incoming_message, name='twillio_mms'),
    path('leads', views.LeadsView.as_view(), name='leads')
]
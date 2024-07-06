from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login', views.Login.as_view(), name='login'),
    path('quote', views.QuoteView.as_view(), name='quote'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('privacy-policy', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('services', views.ServicesView.as_view(), name='services'),
    path('leads', views.LeadsView.as_view(), name='leads'),
    path('<slug:slug>', views.PPCLandingPageView.as_view(), name='ppc')
]
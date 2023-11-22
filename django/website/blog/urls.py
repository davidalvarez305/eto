from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login', views.Login.as_view(), name='login'),
    path('quote', views.QuoteView.as_view(), name='quote'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('privacy-policy', views.ContactView.as_view(), name='contact'),
    path('about', views.HomeView.as_view(), name='about'),
    path('pressure-washing', views.PPCLandingPageView.as_view(), name='pressure_washing')
]
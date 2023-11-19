from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('quote', views.HomeView.as_view(), name='quote'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('privacy-policy', views.ContactView.as_view(), name='contact'),
    path('about', views.HomeView.as_view(), name='about'),
    path('sitemap_index.xml', views.sitemap_index, name='sitemap_index'),
    path('pressure-washing', views.PPCLandingPageView.as_view(), name='pressure_washing'),
    path('<int:int>/sitemap.xml.gz', views.sitemap, name='sitemap'),
    path('<slug:location>', views.LocationView.as_view(), name='location'),
    path('<slug:location>/<slug:service>', views.ServiceLocationView.as_view(), name='service_location')
]
from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<int:int>/sitemap.xml.gz', views.sitemap, name='sitemap'),
    path('sitemap_index.xml', views.sitemap_index, name='sitemap_index')
]
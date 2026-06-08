from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('vesti/<int:pk>', views.vesti, name='vesti'),
    path('about/', views.about, name='about'),
    path('casopis/', views.rec, name='rec'),
    path('casopis/<int:pk>', views.rec_detail, name='rec_detail'),
    path('bioskop/', views.bioskop, name='bioskop'),
    path('bioskop/rezervacija/', views.bioskop_rezervacija, name='bioskop_rezervacija'),
    path('likovna-kolonija/', views.likovna_kolonija, name='likovna_kolonija'),
    path('likovna-kolonija/<slug:slug>/', views.likovna_kolonija_detail, name='likovna_kolonija_detail'),
]

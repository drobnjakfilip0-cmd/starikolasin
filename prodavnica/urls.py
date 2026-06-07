from django.urls import path
from . import views

app_name = 'prodavnica'

urlpatterns = [
    path('', views.market, name='market'),
    path('contact-product/', views.contact_product, name='contact_product')
]
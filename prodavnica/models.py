from django.db import models

# Create your models here.
class Product(models.Model):
    ime = models.CharField(max_length=100)
    opis = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images/')
    cena = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
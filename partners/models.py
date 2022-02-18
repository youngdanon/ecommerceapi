from django.db import models
from main.models import Product


class Partner(models.Model):
    username = models.CharField('username', max_length=100)
    email = models.EmailField('email', max_length=255)
    password = models.CharField('password', max_length=255)
    balance = models.DecimalField('balance', max_digits=100, decimal_places=2)


class Offer(models.Model):
    partner = models.ForeignKey(Partner, related_name='offer', on_delete=models.CASCADE)
    product = models.OneToOneField(Product, related_name='offer', on_delete=models.CASCADE)
    transitions_amount = models.IntegerField('transition')
    orders_amount = models.IntegerField('orders_amount')

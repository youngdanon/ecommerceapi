from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.templatetags.static import static

from users.models import User


class Category(models.Model):
    name = models.CharField('category', max_length=100)
    description = models.TextField('description')
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    SKU = models.IntegerField('sku', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField('name', max_length=255)
    meta_tags = ArrayField(models.CharField(max_length=50))
    description = models.TextField('description')
    price = models.DecimalField('price', max_digits=100, decimal_places=2)
    old_price = models.DecimalField('price', max_digits=100, decimal_places=2, blank=True)
    is_active = models.BooleanField('is_active', default=True)
    stock = models.IntegerField('stock')
    similar_to = models.ManyToManyField(to='self', blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    amount = models.IntegerField('amount')
    datetime = models.DateTimeField('datetime', auto_now=True)
    status = models.CharField('status', max_length=15)


class Feedback(models.Model):
    product = models.ForeignKey(Product, related_name='feedback', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='order', on_delete=models.CASCADE)
    mark = models.IntegerField('mark')
    text = models.TextField('text')


class FeedbackReply(models.Model):
    feedback = models.OneToOneField(Feedback, on_delete=models.CASCADE)
    text = models.TextField('feedback_reply')


class Cart(models.Model):
    product = models.ForeignKey(Product, related_name='cart_product', on_delete=models.CASCADE)
    amount = models.IntegerField('amount')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class ProductImage(models.Model):
    small_image = models.ImageField(upload_to='product/resized/%b%d%Y%H%M%S/',
                                    default=static('no_avatar.png'))
    image = models.ImageField(upload_to='product/%b%d%Y%H%M%S/',
                              default=static('no_avatar.png'))
    product = models.ForeignKey(Product, related_name='image', on_delete=models.CASCADE, null=True, blank=True)


class FeedbackImage(models.Model):
    image = models.ImageField(upload_to='feedback/%b%d%Y%H%M%S/')
    feedback = models.ForeignKey(Feedback, related_name='image', on_delete=models.CASCADE, null=True,
                                 blank=True)

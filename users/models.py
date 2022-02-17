from django.db import models


class User(models.Model):
    username = models.CharField('username', max_length=25, unique=True)
    email = models.EmailField('email', max_length=50, unique=True)
    password = models.CharField('password', max_length=255)
    role = models.CharField('role', max_length=50)

    def __str__(self):
        return self.username


class Profile(models.Model):
    first_name = models.CharField('first name', max_length=50)
    last_name = models.CharField('last name', max_length=50)
    phone = models.CharField('phone', max_length=20, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField("country", max_length=255)
    region = models.CharField("region", max_length=255)
    city = models.CharField("city", max_length=255)
    street = models.CharField("street", max_length=255)
    house = models.CharField("house", max_length=255)
    apartment = models.CharField("apartment", max_length=255, null=True, blank=True)
    zip_code = models.CharField("zip_code", max_length=255)




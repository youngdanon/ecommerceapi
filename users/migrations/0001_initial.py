# Generated by Django 4.0.2 on 2022-02-13 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255, verbose_name='country')),
                ('region', models.CharField(max_length=255, verbose_name='region')),
                ('city', models.CharField(max_length=255, verbose_name='city')),
                ('street', models.CharField(max_length=255, verbose_name='street')),
                ('house', models.CharField(max_length=255, verbose_name='house')),
                ('apartment', models.CharField(blank=True, max_length=255, null=True, verbose_name='apartment')),
                ('zip_code', models.CharField(max_length=255, verbose_name='zip_code')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=25, verbose_name='username')),
                ('email', models.EmailField(max_length=50, verbose_name='email')),
                ('password', models.CharField(max_length=255, verbose_name='password')),
                ('role', models.CharField(max_length=50, verbose_name='role')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
                ('phone', models.CharField(max_length=20, verbose_name='phone')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.user')),
            ],
        ),
    ]
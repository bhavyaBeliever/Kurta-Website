# Generated by Django 5.0.2 on 2024-03-29 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='wishList',
            field=models.ManyToManyField(null=True, to='users.kurta'),
        ),
    ]

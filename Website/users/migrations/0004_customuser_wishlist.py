# Generated by Django 5.0.2 on 2024-03-29 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_kurta_image_kurta_back_kurta_main_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='wishList',
            field=models.ManyToManyField(to='users.kurta'),
        ),
    ]

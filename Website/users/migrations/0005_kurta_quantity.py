# Generated by Django 5.0.2 on 2024-03-08 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='kurta',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
# Generated by Django 5.0.2 on 2024-03-22 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_kurta_size_remove_kurta_stock_cartitem_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='size',
            field=models.CharField(default='s', max_length=3),
        ),
        migrations.AlterField(
            model_name='kurta',
            name='l',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='kurta',
            name='m',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='kurta',
            name='s',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='kurta',
            name='xl',
            field=models.IntegerField(default=1),
        ),
    ]
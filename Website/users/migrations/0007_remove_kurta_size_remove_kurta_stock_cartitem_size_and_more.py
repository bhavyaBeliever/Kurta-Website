# Generated by Django 5.0.2 on 2024-03-22 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_kurta_quantity_cartitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kurta',
            name='size',
        ),
        migrations.RemoveField(
            model_name='kurta',
            name='stock',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='size',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='kurta',
            name='l',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='kurta',
            name='m',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='kurta',
            name='s',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='kurta',
            name='xl',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='kurta',
            name='Occasion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Fest', to='users.festival'),
        ),
    ]

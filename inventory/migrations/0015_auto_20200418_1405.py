# Generated by Django 3.0.5 on 2020-04-18 14:05

from django.db import migrations, models
import inventory.models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_auto_20200416_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=inventory.models.upload_location),
        ),
    ]
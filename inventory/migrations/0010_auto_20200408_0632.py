# Generated by Django 3.0.5 on 2020-04-08 06:32

from django.db import migrations, models
import inventory.models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_item_barcodeimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='barcode',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='item',
            name='barcodeImage',
            field=models.ImageField(blank=True, editable=False, max_length=200, upload_to='barcodes/'),
        ),
    ]

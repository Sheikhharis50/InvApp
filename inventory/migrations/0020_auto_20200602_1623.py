# Generated by Django 3.0.5 on 2020-06-02 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_auto_20200530_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='contact',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.Location'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='contact',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
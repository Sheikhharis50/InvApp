# Generated by Django 3.0.5 on 2020-06-08 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0027_auto_20200607_0319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='demand_items',
            old_name='bundles',
            new_name='stock',
        ),
        migrations.RemoveField(
            model_name='demand',
            name='invoice',
        ),
        migrations.RemoveField(
            model_name='demand_items',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='invoice',
        ),
    ]

# Generated by Django 3.0.5 on 2020-04-07 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase_Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('bundels', models.FloatField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Item')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Purchase')),
            ],
        ),
        migrations.CreateModel(
            name='Order_Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('bundles', models.FloatField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Demand_Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('bundels', models.FloatField()),
                ('demand', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Demand')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.Item')),
            ],
        ),
    ]

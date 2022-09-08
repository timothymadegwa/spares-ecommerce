# Generated by Django 4.0.6 on 2022-09-08 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spares', '0003_alter_inventory_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spares.brand'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spares.category'),
        ),
    ]

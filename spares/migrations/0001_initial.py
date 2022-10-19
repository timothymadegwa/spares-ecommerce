# Generated by Django 4.0.6 on 2022-10-19 14:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('is_ordered', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
                ('shipping_location', models.CharField(max_length=255)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('payment_method', models.CharField(max_length=100)),
                ('paid', models.BooleanField(default=False)),
                ('delivered', models.BooleanField(default=False)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
                ('items', models.ManyToManyField(to='spares.cart')),
                ('shipping_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spares.shipping')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('price', models.FloatField()),
                ('is_displayed', models.BooleanField(default=True)),
                ('has_discount', models.BooleanField(default=False)),
                ('discount', models.FloatField(default=0)),
                ('photo', models.ImageField(upload_to='photos/spares')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spares.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spares.category')),
            ],
            options={
                'verbose_name': 'inventory',
                'verbose_name_plural': 'inventory',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spares.inventory'),
        ),
    ]

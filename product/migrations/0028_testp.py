# Generated by Django 3.2.3 on 2022-07-16 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_rename_product_productvariantdetail_product_variant'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestP',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.product')),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
            ],
            bases=('product.product',),
        ),
    ]

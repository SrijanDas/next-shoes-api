# Generated by Django 3.2.3 on 2022-08-13 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_productimage'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.parentproduct'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=2),
        ),
    ]
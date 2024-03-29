# Generated by Django 3.2.3 on 2022-08-15 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_productimage'),
        ('reviews', '0004_alter_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='show_on_client_side',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.parentproduct'),
        ),
    ]

# Generated by Django 3.2.3 on 2022-08-25 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_alter_returnitem_order_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=256, null=True, unique=True),
        ),
    ]
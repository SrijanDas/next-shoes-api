# Generated by Django 3.2.3 on 2022-08-22 05:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_alter_returnitem_order_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='returnitem',
            name='order_item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='order.orderitem'),
        ),
    ]

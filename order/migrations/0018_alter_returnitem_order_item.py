# Generated by Django 3.2.3 on 2022-08-22 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_auto_20220822_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='returnitem',
            name='order_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.orderitem', unique=True),
        ),
    ]

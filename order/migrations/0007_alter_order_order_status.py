# Generated by Django 3.2.3 on 2021-05-20 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20210520_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('YTD', 'Yet to dispatch'), ('DIS', 'Dispatched'), ('SHP', 'Shipped'), ('CAN', 'Cancelled')], default='YTD', max_length=3),
        ),
    ]

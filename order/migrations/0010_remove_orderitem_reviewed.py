# Generated by Django 3.2.3 on 2022-08-15 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_orderitem_reviewed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='reviewed',
        ),
    ]
# Generated by Django 3.2.3 on 2022-08-04 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20220729_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

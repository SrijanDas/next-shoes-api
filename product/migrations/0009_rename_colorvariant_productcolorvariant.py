# Generated by Django 3.2.3 on 2022-08-15 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_productimage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ColorVariant',
            new_name='ProductColorVariant',
        ),
    ]

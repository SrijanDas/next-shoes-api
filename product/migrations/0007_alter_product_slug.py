# Generated by Django 3.2.3 on 2022-08-07 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_merge_0001_initial_0005_merge_20220806_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]

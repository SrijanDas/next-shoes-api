# Generated by Django 3.2.3 on 2022-07-21 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20220721_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='phone',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]

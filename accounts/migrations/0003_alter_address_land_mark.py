# Generated by Django 3.2.3 on 2022-08-25 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220825_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='land_mark',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

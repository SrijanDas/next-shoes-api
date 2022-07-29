# Generated by Django 3.2.3 on 2022-07-21 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20220721_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='has_shop',
        ),
        migrations.AddField(
            model_name='account',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
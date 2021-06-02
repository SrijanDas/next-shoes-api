# Generated by Django 3.2.3 on 2021-05-21 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_alter_order_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='CancelledOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason_for_cancellation', models.CharField(blank=True, max_length=200, null=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
    ]

# Generated by Django 3.2.3 on 2022-08-13 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_alter_product_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=255)),
                ('color_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.colorvariant')),
            ],
        ),
    ]

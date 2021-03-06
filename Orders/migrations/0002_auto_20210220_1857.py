# Generated by Django 3.1.4 on 2021-02-20 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basket',
            options={'verbose_name': 'Basket', 'verbose_name_plural': 'Basketes'},
        ),
        migrations.AlterModelOptions(
            name='basketitem',
            options={'verbose_name': 'BasketDetail', 'verbose_name_plural': 'BasketDetails'},
        ),
        migrations.AddField(
            model_name='basketitem',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='price'),
        ),
    ]

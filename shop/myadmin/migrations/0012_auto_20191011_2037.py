# Generated by Django 2.1 on 2019-10-11 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0011_auto_20191011_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='adress',
            name='uid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myadmin.Users'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.IntegerField(default=1570797465),
        ),
    ]
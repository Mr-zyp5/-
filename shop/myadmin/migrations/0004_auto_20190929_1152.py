# Generated by Django 2.1 on 2019-09-29 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0003_goods'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='age',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(default='123456', max_length=100),
        ),
        migrations.AlterField(
            model_name='users',
            name='sex',
            field=models.CharField(max_length=1, null=True),
        ),
    ]

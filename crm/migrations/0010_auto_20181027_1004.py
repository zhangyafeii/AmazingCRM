# Generated by Django 2.0.5 on 2018-10-27 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_auto_20181027_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerinfo',
            name='emergence_contract',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='id_num',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='sex',
            field=models.PositiveIntegerField(blank=True, choices=[(0, '男'), (1, '女')], null=True),
        ),
    ]
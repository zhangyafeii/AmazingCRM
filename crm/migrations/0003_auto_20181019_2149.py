# Generated by Django 2.0.5 on 2018-10-19 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20181019_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.CustomerInfo'),
        ),
    ]
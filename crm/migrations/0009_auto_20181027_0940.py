# Generated by Django 2.0.5 on 2018-10-27 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_auto_20181027_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentenrollment',
            name='consultant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.UserProfile'),
        ),
    ]
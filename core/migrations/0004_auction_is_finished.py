# Generated by Django 2.0.4 on 2018-04-26 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20180425_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
    ]

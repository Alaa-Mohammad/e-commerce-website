# Generated by Django 3.2.7 on 2022-01-08 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='details',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='order',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
    ]

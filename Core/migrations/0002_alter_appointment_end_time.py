# Generated by Django 5.0 on 2024-01-04 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='end_time',
            field=models.DateField(),
        ),
    ]
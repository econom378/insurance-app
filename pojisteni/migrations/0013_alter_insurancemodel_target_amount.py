# Generated by Django 4.2.4 on 2023-08-20 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pojisteni', '0012_alter_insurancemodel_target_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurancemodel',
            name='target_amount',
            field=models.IntegerField(default=None, max_length=20),
        ),
    ]

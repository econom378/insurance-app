# Generated by Django 4.2.4 on 2023-08-20 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pojisteni', '0009_alter_insurancemodel_policyholder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insurancemodel',
            name='insurance_object',
        ),
        migrations.AddField(
            model_name='insurancemodel',
            name='target_amount',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='insurancemodel',
            name='insurance_type',
            field=models.CharField(choices=[('Pojištění majetku', 'Pojištění majetku'), ('Životní pojištění', 'Životní pojištění'), ('Cestovní pojištění', 'Cestovní pojištění'), ('Povinné ručení', 'Povinné ručení'), ('Havarijní pojištění', 'Havarijní pojištění'), ('Úrazové pojištění', 'Úrazové pojištění'), ('Jiné pojištění', 'Jiné pojištění')], default='Pojištění majetku', max_length=30),
        ),
    ]
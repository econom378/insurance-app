# Generated by Django 4.2.4 on 2023-08-20 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pojisteni', '0003_alter_policyholder_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsuranceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insurance_type', models.CharField(choices=[('PM', 'Pojištění majetku'), ('ZP', 'Životní pojištění'), ('CP', 'Cestovní pojištění'), ('PR', 'Povinné ručení'), ('HP', 'Havarijní pojištění'), ('UP', 'Úrazové pojištění'), ('JP', 'Jiné pojištění')], default='PM', max_length=2)),
                ('insurance_object', models.CharField(max_length=30)),
                ('valid_from', models.DateField()),
                ('valid_to', models.DateField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('policyholder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pojisteni.policyholder')),
            ],
        ),
    ]

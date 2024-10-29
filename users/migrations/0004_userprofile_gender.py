# Generated by Django 5.1.1 on 2024-10-29 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_blood_pressure_userprofile_doctor_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('No Choice', 'No Choice'), ('M', 'Male'), ('F', 'Female'), ('Other', 'Other')], default='No Choice', max_length=100),
        ),
    ]
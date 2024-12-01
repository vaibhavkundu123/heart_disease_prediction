# Generated by Django 5.1.1 on 2024-11-26 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_predictionresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='predictionresult',
            name='symptoms',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='predictionresult',
            name='existing_conditions',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='predictionresult',
            name='family_history',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='predictionresult',
            name='predicted_disease',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='predictionresult',
            name='smoking_status',
            field=models.CharField(default='Unknown', max_length=255),
        ),
    ]
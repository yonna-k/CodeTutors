# Generated by Django 5.1.2 on 2024-12-06 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0013_booking_tutor_tutor_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='tutor',
        ),
        migrations.RemoveField(
            model_name='tutor',
            name='students',
        ),
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('OPEN', 'OPEN'), ('CLOSED', 'CLOSED')], default='OPEN', max_length=10),
        ),
    ]
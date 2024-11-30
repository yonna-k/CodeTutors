# Generated by Django 5.1.2 on 2024-11-27 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0008_booking_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='lang',
            field=models.CharField(choices=[('Python', 'Python'), ('Java', 'Java'), ('Ruby', 'Ruby'), ('C', 'C'), ('SQL', 'SQL')], default='Python', max_length=20),
        ),
    ]

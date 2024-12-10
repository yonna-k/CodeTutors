# Generated by Django 5.1.2 on 2024-12-10 11:54

import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message='Username must consist of @ followed by at least three alphanumericals', regex='^@\\w{3,}$')])),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('tutor', 'Tutor'), ('student', 'Student')], default='student', max_length=15)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='admin_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='student_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('level', models.CharField(choices=[('BEGINNER', 'Beginner'), ('INTERMEDIATE', 'Intermediate'), ('ADVANCED', 'Advanced')], default='BEGINNER', max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='tutor_profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('specializes_in_python', models.BooleanField(default=False)),
                ('specializes_in_java', models.BooleanField(default=False)),
                ('specializes_in_C', models.BooleanField(default=False)),
                ('specializes_in_ruby', models.BooleanField(default=False)),
                ('specializes_in_SQL', models.BooleanField(default=False)),
                ('available_monday', models.BooleanField(default=False)),
                ('available_tuesday', models.BooleanField(default=False)),
                ('available_wednesday', models.BooleanField(default=False)),
                ('available_thursday', models.BooleanField(default=False)),
                ('available_friday', models.BooleanField(default=False)),
                ('available_saturday', models.BooleanField(default=False)),
                ('available_sunday', models.BooleanField(default=False)),
                ('rate', models.DecimalField(decimal_places=2, help_text='Enter your preferred hourly rate: ', max_digits=5, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('venue', models.CharField(default='Code Tutors HQ', max_length=100)),
                ('status', models.CharField(choices=[('OPEN', 'OPEN'), ('CLOSED', 'CLOSED')], default='OPEN', max_length=10)),
                ('frequency', models.CharField(choices=[('weekly', 'weekly'), ('fortnightly', 'fortnightly')], default='weekly', max_length=20)),
                ('duration', models.CharField(choices=[('short', 'short (1hr)'), ('long', 'long (2hrs)')], default='short', max_length=10)),
                ('day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')], default='Monday', max_length=20)),
                ('lang', models.CharField(choices=[('Python', 'Python'), ('Java', 'Java'), ('Ruby', 'Ruby'), ('C', 'C'), ('SQL', 'SQL')], default='Python', max_length=20)),
                ('student', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='tutorials.student')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='lesson', serialize=False, to='tutorials.booking')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorials.tutor')),
            ],
        ),
    ]

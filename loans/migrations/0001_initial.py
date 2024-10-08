# Generated by Django 5.1.1 on 2024-09-17 00:49

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('national_id', models.CharField(max_length=20, unique=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('credit_score', models.IntegerField(default=0)),
                ('employment_status', models.CharField(blank=True, choices=[('Employed', 'Employed'), ('Self-Employed', 'Self-Employed')], max_length=50, null=True)),
                ('income', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('loan_eligibility_status', models.BooleanField(default=False)),
                ('referral_code', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('referred_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referrals', to='loans.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

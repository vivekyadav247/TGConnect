# Generated by Django 5.2.1 on 2025-07-26 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='addreports',
            fields=[
                ('enroll', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('branch', models.CharField(max_length=20)),
                ('sem', models.IntegerField()),
                ('cgpa', models.FloatField()),
                ('filename', models.CharField(max_length=100)),
                ('info', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enroll', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=10)),
                ('tg_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=20)),
                ('subject', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=50, unique=True)),
                ('filename', models.CharField(max_length=50)),
                ('info', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('notice_file', models.FileField(upload_to='notifications/')),
                ('info', models.CharField(max_length=200)),
                ('expiry_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('enroll', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=100)),
                ('course', models.CharField(max_length=20)),
                ('branch', models.CharField(max_length=20)),
                ('year', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=10)),
                ('status', models.IntegerField()),
                ('role', models.CharField(max_length=10)),
                ('info', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RegisterTG',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile', models.CharField(max_length=15)),
                ('course', models.CharField(max_length=20)),
                ('department', models.CharField(max_length=20)),
                ('year', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=10)),
                ('status', models.IntegerField(default=0)),
                ('role', models.CharField(max_length=10)),
                ('info', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=20)),
                ('month', models.CharField(max_length=10)),
                ('week', models.CharField(max_length=10)),
                ('fromdate', models.CharField(max_length=20)),
                ('todate', models.CharField(max_length=20)),
                ('filename', models.CharField(max_length=20)),
                ('info', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UploadAssignment',
            fields=[
                ('enroll', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('branch', models.CharField(max_length=20)),
                ('subject', models.CharField(max_length=25)),
                ('filename', models.CharField(max_length=40)),
                ('verify', models.IntegerField()),
                ('info', models.CharField(max_length=45)),
            ],
        ),
    ]

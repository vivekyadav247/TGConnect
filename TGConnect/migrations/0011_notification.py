# Generated by Django 5.2.1 on 2025-06-01 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGConnect', '0010_attendance'),
    ]

    operations = [
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
    ]

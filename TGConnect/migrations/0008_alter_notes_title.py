# Generated by Django 5.2.1 on 2025-05-30 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGConnect', '0007_notes_timetable_id_alter_timetable_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]

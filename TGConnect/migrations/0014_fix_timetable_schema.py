# Generated migration to fix database schema issues

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TGConnect', '0013_alter_register_mobile_alter_registertg_department_and_more'),
    ]

    operations = [
        # Drop all existing tables to avoid conflicts
        migrations.RunSQL(
            "DROP TABLE IF EXISTS TGConnect_timetable CASCADE;",
            reverse_sql="SELECT 1;"
        ),
        migrations.RunSQL(
            "DROP TABLE IF EXISTS TGConnect_notes CASCADE;", 
            reverse_sql="SELECT 1;"
        ),
        migrations.RunSQL(
            "DROP TABLE IF EXISTS TGConnect_uploadassignment CASCADE;",
            reverse_sql="SELECT 1;"
        ),
        migrations.RunSQL(
            "DROP TABLE IF EXISTS TGConnect_attendance CASCADE;",
            reverse_sql="SELECT 1;"
        ),
        migrations.RunSQL(
            "DROP TABLE IF EXISTS TGConnect_notification CASCADE;",
            reverse_sql="SELECT 1;"
        ),
        
        # Recreate TimeTable with proper primary key
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('department', models.CharField(max_length=20)),
                ('month', models.CharField(max_length=10)),
                ('week', models.CharField(max_length=10)),
                ('fromdate', models.CharField(max_length=20)),
                ('todate', models.CharField(max_length=20)),
                ('filename', models.CharField(max_length=20)),
                ('info', models.CharField(max_length=50)),
            ],
        ),
    ]

# Generated by Django 3.0.3 on 2020-08-27 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0002_auto_20200827_1143'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Answers',
            new_name='Answer',
        ),
        migrations.RenameModel(
            old_name='Frames',
            new_name='Frame',
        ),
        migrations.RenameModel(
            old_name='Options',
            new_name='Option',
        ),
        migrations.RenameModel(
            old_name='Questions',
            new_name='Question',
        ),
        migrations.RenameModel(
            old_name='Subjects',
            new_name='Subject',
        ),
        migrations.RenameModel(
            old_name='Topics',
            new_name='Topic',
        ),
        migrations.RenameModel(
            old_name='Videos',
            new_name='Video',
        ),
    ]

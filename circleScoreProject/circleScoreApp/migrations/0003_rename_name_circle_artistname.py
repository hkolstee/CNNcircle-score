# Generated by Django 4.1.3 on 2022-11-04 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circleScoreApp', '0002_circle_draw_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='circle',
            old_name='name',
            new_name='artistName',
        ),
    ]

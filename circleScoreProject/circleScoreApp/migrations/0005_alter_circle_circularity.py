# Generated by Django 4.1.3 on 2022-11-04 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circleScoreApp', '0004_alter_circle_circularity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circle',
            name='circularity',
            field=models.DecimalField(decimal_places=6, max_digits=7),
        ),
    ]
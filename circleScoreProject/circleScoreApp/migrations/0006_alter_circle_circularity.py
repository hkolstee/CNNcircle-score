# Generated by Django 4.1.3 on 2022-11-04 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circleScoreApp', '0005_alter_circle_circularity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circle',
            name='circularity',
            field=models.DecimalField(decimal_places=10, max_digits=11),
        ),
    ]

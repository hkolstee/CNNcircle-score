# Generated by Django 4.1.3 on 2022-11-03 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('circularity', models.IntegerField()),
                ('circle', models.ImageField(upload_to='circles/')),
            ],
        ),
    ]

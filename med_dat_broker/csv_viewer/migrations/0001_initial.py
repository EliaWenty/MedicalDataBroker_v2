# Generated by Django 2.2.7 on 2020-01-04 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='csvModel',
            fields=[
                ('c_uuid', models.AutoField(primary_key=True, serialize=False)),
                ('c_name', models.CharField(max_length=50)),
            ],
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-16 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('studentName', models.CharField(blank=True, max_length=30, null=True)),
                ('connectionID', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
    ]

# Generated by Django 4.2.1 on 2023-08-06 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='file',
            field=models.FileField(blank=True, max_length=50, null=True, upload_to=None),
        ),
    ]

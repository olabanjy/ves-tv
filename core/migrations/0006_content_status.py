# Generated by Django 3.2.9 on 2023-09-23 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20230923_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='status',
            field=models.TextField(choices=[('Uploading', 'Uploading'), ('Submitted', 'Submitted'), ('In Review', 'In Review'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Removed', 'Removed')], default='Approved', verbose_name='status'),
        ),
    ]

# Generated by Django 3.2.9 on 2023-10-15 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_profile_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

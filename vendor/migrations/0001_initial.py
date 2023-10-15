# Generated by Django 3.2.9 on 2023-10-15 06:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0007_profile_company_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contracts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_file', models.FileField(blank=True, null=True, upload_to='vendor/contracts')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
# Generated by Django 3.2.9 on 2023-10-19 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_profile_company_alias'),
        ('vendor', '0004_bankaccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(blank=True, max_length=100, null=True)),
                ('banner', models.ImageField(blank=True, upload_to='channel/banner')),
                ('total_views', models.IntegerField(default=0)),
                ('verified', models.BooleanField(default=False)),
                ('about', models.TextField(blank=True, null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
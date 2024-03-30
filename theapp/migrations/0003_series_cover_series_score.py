# Generated by Django 4.1.7 on 2024-03-30 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theapp', '0002_profile_books'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='cover',
            field=models.FileField(blank=True, default='cover/default.png', upload_to='cover/'),
        ),
        migrations.AddField(
            model_name='series',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]

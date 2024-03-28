# Generated by Django 4.1.7 on 2024-03-28 04:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference', models.TextField(blank=True, null=True)),
                ('blacklist', models.TextField(blank=True, null=True)),
                ('avatar', models.FileField(default='avatar/default-avatar.png', upload_to='avatar/')),
                ('account_created', models.DateField(blank=True, null=True)),
                ('username', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('author', models.CharField(max_length=40)),
                ('status', models.CharField(choices=[('FINISH', 'FINISH'), ('ON-GOING', 'ON-GOING')], max_length=20)),
                ('pub_jp', models.CharField(blank=True, max_length=20, null=True)),
                ('pub_en', models.CharField(blank=True, max_length=20, null=True)),
                ('genre', models.CharField(max_length=110, null=True)),
                ('desc', models.TextField(default='-', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('uniq', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('volume', models.IntegerField()),
                ('synopsis', models.TextField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='theapp.series')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(max_length=300)),
                ('score', models.DecimalField(decimal_places=1, max_digits=2)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theapp.profile')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theapp.series')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(max_length=100)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theapp.profile')),
                ('volume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theapp.volume')),
            ],
        ),
    ]
# Generated by Django 5.2.3 on 2025-06-18 21:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('party', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('votes', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['-votes', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=101)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('has_voted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voted_at', models.DateTimeField(auto_now_add=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_votes', to='voting.candidate')),
                ('voter', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vote', to='voting.voter')),
            ],
            options={
                'unique_together': {('voter',)},
            },
        ),
    ]

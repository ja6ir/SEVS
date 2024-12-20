# Generated by Django 4.1.3 on 2024-03-07 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('JBApp', '0008_election_election_date_alter_election_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Objection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=400)),
                ('date', models.DateField(auto_now_add=True)),
                ('election', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='JBApp.election')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JBApp.student')),
            ],
        ),
    ]

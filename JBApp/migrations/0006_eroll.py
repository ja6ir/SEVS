# Generated by Django 4.1.3 on 2024-03-06 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('JBApp', '0005_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='ERoll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('date', models.DateField(auto_now_add=True)),
                ('hodsign', models.CharField(default='Not approved', max_length=20)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='JBApp.faculty')),
            ],
        ),
    ]
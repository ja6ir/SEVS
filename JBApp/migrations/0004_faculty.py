# Generated by Django 4.1.3 on 2024-03-06 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('JBApp', '0003_remove_hod_department_hod_dptmnt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('contact', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=20)),
                ('dptmnt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='JBApp.department')),
                ('usr_con', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

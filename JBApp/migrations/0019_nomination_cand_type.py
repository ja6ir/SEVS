# Generated by Django 5.0.4 on 2024-04-07 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JBApp', '0018_nomination_noofvotesno'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomination',
            name='cand_type',
            field=models.CharField(max_length=15, null=True),
        ),
    ]

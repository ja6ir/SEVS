# Generated by Django 4.1.3 on 2024-03-08 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JBApp', '0016_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomination',
            name='noOfVotes',
            field=models.IntegerField(default=0, null=True),
        ),
    ]

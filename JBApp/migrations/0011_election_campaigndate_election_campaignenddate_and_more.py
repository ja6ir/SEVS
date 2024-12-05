# Generated by Django 4.1.3 on 2024-03-07 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JBApp', '0010_remove_election_election_date_dates'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='campaignDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='election',
            name='campaignEndDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='election',
            name='election_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='election',
            name='erollAddDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='election',
            name='nomiWithdrawDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='election',
            name='nominationDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='election',
            name='objectionAcceptDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='election',
            name='resultPublishingDate',
            field=models.DateField(null=True),
        ),
        migrations.DeleteModel(
            name='Dates',
        ),
    ]

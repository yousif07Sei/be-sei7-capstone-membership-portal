# Generated by Django 4.2.7 on 2024-01-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('be_api_members', '0003_alter_profile_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='status',
            field=models.CharField(choices=[(0, 'Pending'), (1, 'Active'), (2, 'Hidden')], default=0, max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Active'), (2, 'Hidden')], default=0),
        ),
    ]

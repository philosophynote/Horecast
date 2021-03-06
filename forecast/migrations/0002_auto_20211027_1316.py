# Generated by Django 3.2.5 on 2021-10-27 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sanrentan',
            old_name='return_field',
            new_name='return_1',
        ),
        migrations.RenameField(
            model_name='umaren',
            old_name='return_field',
            new_name='return_1',
        ),
        migrations.RenameField(
            model_name='umatan',
            old_name='return_field',
            new_name='return_1',
        ),
        migrations.AddField(
            model_name='sanrentan',
            name='return_2',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sanrentan',
            name='win_4',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sanrentan',
            name='win_5',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sanrentan',
            name='win_6',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='umaren',
            name='return_2',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='umaren',
            name='win_3',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='umaren',
            name='win_4',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='umatan',
            name='return_2',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='umatan',
            name='win_3',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='umatan',
            name='win_4',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]

# Generated by Django 3.1.4 on 2023-02-21 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ServerAPI', '0003_auto_20230221_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detector',
            name='idd',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='swan',
            name='idd',
            field=models.IntegerField(),
        ),
    ]
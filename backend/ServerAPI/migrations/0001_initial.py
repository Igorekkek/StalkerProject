# Generated by Django 3.1.4 on 2023-02-21 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Swan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField(blank=True, null=True)),
                ('y', models.IntegerField(blank=True, null=True)),
                ('_id', models.IntegerField(unique=True)),
                ('int0', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Detector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField(blank=True, null=True)),
                ('y', models.IntegerField(blank=True, null=True)),
                ('_id', models.IntegerField(unique=True)),
                ('swans', models.ManyToManyField(blank=True, to='ServerAPI.Swan')),
            ],
        ),
    ]

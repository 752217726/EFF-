# Generated by Django 2.0.6 on 2020-05-03 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('pwd', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=30)),
                ('salt', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'tb_users',
            },
        ),
    ]

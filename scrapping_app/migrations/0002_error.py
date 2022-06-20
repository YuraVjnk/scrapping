# Generated by Django 4.0.5 on 2022-06-04 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapping_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Ошибка',
                'verbose_name_plural': 'Ошибки',
            },
        ),
    ]
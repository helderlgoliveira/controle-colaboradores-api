# Generated by Django 3.2.7 on 2021-09-13 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localidades_brasileiras', '0002_alter_unidadefederativa_capital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipio',
            name='nome',
            field=models.CharField(max_length=200, verbose_name='Nome do Município'),
        ),
    ]

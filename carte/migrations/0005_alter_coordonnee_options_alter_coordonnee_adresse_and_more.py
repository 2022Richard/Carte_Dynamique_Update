# Generated by Django 5.0.4 on 2024-04-04 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0004_coordonnee_adresse_coordonnee_nom'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coordonnee',
            options={'ordering': ['Nom']},
        ),
        migrations.AlterField(
            model_name='coordonnee',
            name='Adresse',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='coordonnee',
            name='Nom',
            field=models.CharField(max_length=200),
        ),
    ]
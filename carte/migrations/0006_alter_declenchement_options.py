# Generated by Django 5.0.4 on 2024-04-04 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carte', '0005_alter_coordonnee_options_alter_coordonnee_adresse_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='declenchement',
            options={'ordering': ['NOM_CLIENT']},
        ),
    ]

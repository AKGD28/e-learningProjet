# Generated by Django 4.2.17 on 2024-12-28 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_alter_chapitre_id_alter_classe_id_alter_cours_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cours',
            name='chapitre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.chapitre'),
        ),
    ]

# Generated by Django 5.1.6 on 2025-05-20 10:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appdata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='formations',
            name='categorie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appdata.project_categ'),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-08 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0004_rename_comentarios_comentario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='contenido',
            field=models.CharField(max_length=50000),
        ),
        migrations.AlterField(
            model_name='post',
            name='resumen',
            field=models.TextField(max_length=50000),
        ),
    ]
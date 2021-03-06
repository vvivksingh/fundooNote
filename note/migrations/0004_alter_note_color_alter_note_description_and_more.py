# Generated by Django 4.0.2 on 2022-06-14 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0003_note_color_note_is_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='color',
            field=models.CharField(blank=True, default='red', max_length=20),
        ),
        migrations.AlterField(
            model_name='note',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]

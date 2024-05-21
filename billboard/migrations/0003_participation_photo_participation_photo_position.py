# Generated by Django 4.2.11 on 2024-05-21 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0002_alter_participation_relationship'),
    ]

    operations = [
        migrations.AddField(
            model_name='participation',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos'),
        ),
        migrations.AddField(
            model_name='participation',
            name='photo_position',
            field=models.CharField(choices=[('left', 'Left'), ('right', 'Right')], default='left', max_length=5),
        ),
    ]

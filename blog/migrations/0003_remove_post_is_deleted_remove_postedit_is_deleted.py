# Generated by Django 4.0.5 on 2022-06-12 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_rename_state_post_status_alter_post_cover_picture_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='postedit',
            name='is_deleted',
        ),
    ]

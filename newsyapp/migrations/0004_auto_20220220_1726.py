# Generated by Django 3.2.11 on 2022-02-20 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsyapp', '0003_alter_comment_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='kids',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]

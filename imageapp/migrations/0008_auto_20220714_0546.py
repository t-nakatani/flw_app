# Generated by Django 3.2.13 on 2022-07-14 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imageapp', '0007_imagemodel_re_estimate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagemodel',
            name='author',
        ),
        migrations.RemoveField(
            model_name='imagemodel',
            name='name',
        ),
    ]

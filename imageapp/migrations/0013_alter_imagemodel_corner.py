# Generated by Django 3.2.13 on 2022-07-24 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageapp', '0012_auto_20220724_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='corner',
            field=models.ImageField(default='', upload_to=''),
        ),
    ]

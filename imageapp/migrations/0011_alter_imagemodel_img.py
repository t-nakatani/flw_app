# Generated by Django 3.2.13 on 2022-07-22 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageapp', '0010_auto_20220722_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='img',
            field=models.ImageField(default='data/img.png', upload_to=''),
        ),
    ]

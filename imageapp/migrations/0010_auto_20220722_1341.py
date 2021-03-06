# Generated by Django 3.2.13 on 2022-07-22 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageapp', '0009_imagemodel_corner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagemodel',
            name='re_estimate',
        ),
        migrations.AddField(
            model_name='imagemodel',
            name='new_corner',
            field=models.ImageField(default='data/img_new_corner.png', upload_to=''),
        ),
        migrations.AddField(
            model_name='imagemodel',
            name='new_lr',
            field=models.ImageField(default='data/img_new_lr.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='imagemodel',
            name='bb',
            field=models.ImageField(default='data/img_bb.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='imagemodel',
            name='corner',
            field=models.ImageField(default='data/img_corner.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='imagemodel',
            name='fore',
            field=models.ImageField(default='data/img_fore.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='imagemodel',
            name='lr',
            field=models.ImageField(default='data/img_lr.png', upload_to=''),
        ),
    ]

# Generated by Django 3.2 on 2021-05-11 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_post_date_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='PDFfile',
            field=models.FileField(upload_to=''),
        ),
    ]

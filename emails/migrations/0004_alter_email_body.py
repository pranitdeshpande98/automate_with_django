# Generated by Django 5.0.2 on 2024-03-09 23:03

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0003_alter_email_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='body',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
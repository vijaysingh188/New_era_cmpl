# Generated by Django 3.0 on 2020-09-01 07:57

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='register_link',
            field=jsonfield.fields.JSONField(blank=True),
        ),
    ]
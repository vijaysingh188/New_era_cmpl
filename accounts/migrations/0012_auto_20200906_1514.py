# Generated by Django 3.0 on 2020-09-06 09:44

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20200906_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='register_link',
            field=jsonfield.fields.JSONField(blank=True, default=[], null=True),
        ),
    ]

# Generated by Django 2.2.12 on 2020-08-28 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='register_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
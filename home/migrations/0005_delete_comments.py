# Generated by Django 3.0.4 on 2020-03-15 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_roles_user_roles'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comments',
        ),
    ]
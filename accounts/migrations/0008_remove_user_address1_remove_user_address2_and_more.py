# Generated by Django 4.0 on 2022-11-08 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_alter_user_zipcode"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="address1",
        ),
        migrations.RemoveField(
            model_name="user",
            name="address2",
        ),
        migrations.RemoveField(
            model_name="user",
            name="phone_number",
        ),
        migrations.RemoveField(
            model_name="user",
            name="zipcode",
        ),
    ]

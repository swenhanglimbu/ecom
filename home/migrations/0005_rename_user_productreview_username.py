# Generated by Django 4.1.4 on 2023-01-02 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_productreview_slug"),
    ]

    operations = [
        migrations.RenameField(
            model_name="productreview",
            old_name="user",
            new_name="username",
        ),
    ]

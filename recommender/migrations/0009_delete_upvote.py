# Generated by Django 3.2.12 on 2022-03-10 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0008_upvote'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Upvote',
        ),
    ]
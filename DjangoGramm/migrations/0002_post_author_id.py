# Generated by Django 4.2.7 on 2023-11-13 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoGramm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

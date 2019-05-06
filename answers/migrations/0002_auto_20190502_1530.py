# Generated by Django 2.2.1 on 2019-05-02 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answers',
            old_name='answer',
            new_name='negative_answer',
        ),
        migrations.AddField(
            model_name='answers',
            name='positive_answer',
            field=models.CharField(default=4, max_length=128),
            preserve_default=False,
        ),
    ]

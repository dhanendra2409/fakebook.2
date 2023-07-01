# Generated by Django 4.2.2 on 2023-06-30 10:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_posts_liked_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='liked_by',
            field=models.ManyToManyField(blank=True, null=True, related_name='like', to=settings.AUTH_USER_MODEL),
        ),
    ]

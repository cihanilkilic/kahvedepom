# Generated by Django 5.1.2 on 2024-11-02 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='mahalle',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Mahalle'),
        ),
    ]

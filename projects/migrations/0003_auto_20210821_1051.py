# Generated by Django 3.2.6 on 2021-08-21 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patron',
            name='total_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='option',
            name='amount',
            field=models.IntegerField(),
        ),
    ]
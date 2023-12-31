# Generated by Django 4.2.4 on 2023-09-05 07:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemon', '0003_remove_menuitem_inventory_menuitem_feature_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='feature',
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(db_index=True, default=datetime.datetime.now),
        ),
    ]

# Generated by Django 4.1 on 2022-10-02 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_app', '0006_address_customer_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(db_column='category_name', max_length=50)),
                ('sub_category_name', models.CharField(db_column='category_img', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='all_products',
            name='product_subcategory',
            field=models.CharField(db_column='sub_category', default='basic', max_length=50),
            preserve_default=False,
        ),
    ]

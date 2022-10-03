# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.db import models

# specifying choices

GENDER_CHOICES = (
    ("all", "All"),
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
)
IsTRUSTED = (
    ("yes", "Yes"),
    ("no", "No"),
)
user_choice = (
    ("admin", "Admin"),
    ("customer", "Customer"),
)
customer_status_choice = (
    ("active", "Active"),
    ("block", "Block"),
)
PRODUCT_STATUS = (
    ("available", "Available"),
    ("not_available", "Not Available"),
)
Bannertype = (
    ("offers","offers"),
    ("special_discounts","special_discounts"),
    ("clearance","clearance"),
    ("time_deals","time_deals"),
)

AVAILABLE_CATEGORY = (
    ("headphone", "Headphone"),
    ("smartphone", "Smartphone"),
    ("modules", "Modules"),
    ("components", "Components"),
    ("electronic_kit", "Electronic Kit"),
    ("sensors", "Sensors"),
    ("lights", "Lights"),
    ("motors", "Motors"),
    ("drone_kit", "Drone Kit"),
)


# declaring a Student Model


class all_products(models.Model):
    product_id = models.AutoField(primary_key=True, db_column='product_id')
    product_name = models.CharField(db_column='Product_Name', max_length=20)  # Field name made lowercase.
    product_description = models.CharField(max_length=50, db_column='product_description')
    product_image1 = models.ImageField(upload_to='product_images/', db_column='product_image1')
    product_image2 = models.ImageField(upload_to='product_images/', db_column='product_image2')
    product_image3 = models.ImageField(upload_to='product_images/', db_column='product_image3')
    product_image4 = models.ImageField(upload_to='product_images/', db_column='product_image4')
    product_arrival_time = models.TextField(db_column='product_arrival_time')
    product_price = models.IntegerField(db_column='product_price')
    product_category = models.CharField(
        max_length=20,
        choices=AVAILABLE_CATEGORY,
        default='drone_kit',
    )
    product_subcategory = models.CharField(max_length=50,db_column='sub_category')
    product_specification_1 = models.CharField(max_length=20, db_column='product_specification_1')
    product_specification_2 = models.CharField(max_length=20, db_column='product_specification_2')
    product_gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default='All',
    )
    product_stock_available = models.IntegerField(db_column='product_stock_available')
    product_rating = models.CharField(max_length=30, db_column='product_rating')
    product_total_sold = models.IntegerField(db_column='product_total_sold')
    product_is_trusted = models.CharField(
        max_length=20,
        choices=IsTRUSTED,
        default='1',
    )
    product_review_id = models.IntegerField(db_column='product_review_id')
    product_status = models.CharField(
        max_length=20,
        choices=PRODUCT_STATUS,
        default='available',
    )


class Cart(models.Model):
    bag_id = models.AutoField(primary_key=True, db_column='bag_id')
    bag_customer_id = models.IntegerField(db_column='bag_customer_id')
    bag_product_id = models.IntegerField(db_column='bag_product_id')
    bag_quantity = models.IntegerField(db_column='bag_quantity')
    total_price = models.IntegerField(db_column='total_price')


class Company_Info(models.Model):
    company_logo = models.ImageField(upload_to='company_logo/', db_column='company_logo')
    company_name = models.CharField(max_length=10, db_column='company_name')
    company_description = models.CharField(max_length=10, db_column='company_description')


class Country(models.Model):
    country_id = models.CharField(max_length=50, db_column='country_id')
    country_name = models.CharField(max_length=50, db_column='country_name')
    country_is_active = models.CharField(max_length=50, db_column='country_is_active')


class Customer(models.Model):
    customer_password = models.CharField(max_length=15, db_column='customer_password')
    customer_phone_number = models.CharField(max_length=40, db_column='customer_phone_number')
    customer_alternative_phone_number = models.CharField(max_length=40, db_column='customer_alternative_phone_number',
                                                         blank=True, null=True)
    customer_email = models.CharField(max_length=20, db_column='customer_email')
    customer_building_id = models.CharField(max_length=20, db_column='customer_building_id')
    customer_landmark = models.CharField(max_length=20, db_column='customer_landmark')
    customer_street = models.CharField(max_length=20, db_column='customer_street')
    customer_city = models.CharField(max_length=20, db_column='customer_city')
    customer_country = models.CharField(max_length=20, db_column='customer_country')
    customer_pincode = models.CharField(max_length=20, db_column='customer_pincode')
    customer_total_buyed = models.CharField(max_length=20, db_column='customer_total_buyed')
    customer_status = models.CharField(
        max_length=20,
        choices=customer_status_choice,
        default='active',
    )
    is_admin = models.CharField(
        max_length=20,
        choices=user_choice,
        default='customer',
    )


class Address(models.Model):
    customer_email = models.CharField(max_length=20, db_column='customer_email')
    customer_first_name = models.CharField(max_length=10, db_column='customer_first_name')
    customer_last_name = models.CharField(max_length=10, db_column='customer_last_name')
    customer_building_id = models.CharField(max_length=20, db_column='customer_building_id')
    customer_landmark = models.CharField(max_length=20, db_column='customer_landmark')
    customer_street = models.CharField(max_length=20, db_column='customer_street')
    customer_city = models.CharField(max_length=20, db_column='customer_city')
    customer_country = models.CharField(max_length=20, db_column='customer_country')
    customer_pincode = models.CharField(max_length=20, db_column='customer_pincode')


class Orders(models.Model):
    order_customer_id = models.IntegerField(db_column='order_customer_id')
    order_product_id = models.IntegerField(db_column='order_product_id')
    order_quantity = models.IntegerField(db_column='order_quantity')
    order_total_price = models.IntegerField(db_column='order_total_price')
    order_ordered_time = models.CharField(max_length=10, db_column='order_ordered_time')
    order_expected_time = models.CharField(max_length=10, db_column='order_expected_time')
    order_delivery_status = models.CharField(max_length=20, db_column='order_delivery_status')


class ReviewTable(models.Model):
    review_id = models.AutoField(primary_key=True, db_column='review_id')
    review_customer_id = models.IntegerField(db_column='review_customer_id')
    review_content = models.CharField(max_length=100, db_column='review_content')


class banner(models.Model):
    banner_type = models.CharField(choices=Bannertype,default='offers',max_length=20)
    banner_name = models.CharField(max_length=50, db_column='banner_name')
    banner_img = models.ImageField(upload_to='banner/', db_column='banner_img')


class Category(models.Model):
    category_name = models.CharField(max_length=50, db_column='category_name')
    category_img = models.ImageField(upload_to='category/', db_column='category_img')

class Subcategory(models.Model):
    category_name = models.CharField(max_length=50, db_column='category_name')
    sub_category_name = models.CharField(max_length=50, db_column='category_img')


class Recommented_Products(models.Model):
    customer_id = models.IntegerField(db_column='customer_id')
    recommented_product_id = models.IntegerField(db_column='recommented_product_id')

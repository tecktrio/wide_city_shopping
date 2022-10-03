from django import forms

from shopping_app.models import all_products, banner, Company_Info, Category, Customer, Subcategory


class add_product_form(forms.ModelForm):
    class Meta:
        model = all_products
        fields = ['product_name', 'product_description', 'product_image1', 'product_image2', 'product_image3',
                  'product_image4', 'product_price', 'product_category', 'product_subcategory',
                  'product_arrival_time', 'product_specification_1', 'product_specification_2',
                  'product_stock_available', 'product_rating', 'product_total_sold', 'product_is_trusted',
                  'product_review_id', 'product_status']


class add_customer_form(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_email', 'customer_password', 'customer_phone_number', 'customer_building_id',
                  'customer_landmark', 'customer_street',
                  'customer_city', 'customer_country', 'customer_pincode', 'customer_total_buyed',
                  'customer_status', 'is_admin']


class add_banner(forms.ModelForm):
    class Meta:
        model = banner
        fields = ['banner_name', 'banner_img', 'banner_type']


class company_info(forms.ModelForm):
    class Meta:
        model = Company_Info
        fields = ['company_logo', 'company_name', 'company_description']


class add_category(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_img', 'category_name']


class handle_subcategory(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['category_name', 'sub_category_name']

import random

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.views.decorators.cache import never_cache

from shopping_app.forms import add_banner, company_info, add_product_form, add_category, add_customer_form, \
    handle_subcategory
from shopping_app.models import banner, Company_Info, all_products, Customer, Category, \
    Recommented_Products, Cart, Orders, Address, Subcategory

product_image_src = []
cart_products = []
recommented_product = []
selected_category = 'all'
customer = ''
otp = ''
product = ''
current_customer = ''
current_product = ''
login_status = 'Login'

# def ajax_get_view(request): # May include more arguments depending on URL parameters
#     # Get data from the database - Ex. Model.object.get(...)
#     data = {
#             'my_data':data_to_display
#     }
#     return JsonResponse(data)
# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


@never_cache
def home(request):
    # global variables, change carefully
    banner_id = 9  # banner id can be in the range of 1 to 5, change this value according to the banner that you want

    # check user status
    current_user = 'guest'
    if 'user' in request.session:
        current_user = request.session['user']

    print('current_user', current_user)
    try:
        current_user = Customer.objects.get(customer_email=current_user)
        # print(current_user.id)
    except:
        current_user = 'guest'

    banners = banner.objects.all()
    company_details = Company_Info.objects.get(id=5)
    print(company_details.company_name)
    products = all_products.objects.all()
    product_category = Category.objects.all()

    try:
        user_recommented_data = Recommented_Products.objects.filter(customer_id=current_user.id)
        for data in user_recommented_data:
            # print(dir(data))
            re_products = all_products.objects.get(product_id=data.recommented_product_id)

            if re_products not in recommented_product:
                recommented_product.append(re_products)
    except:
        pass

    set_new_arrival_date = '2022-09-30'
    context = {'banners': banners, 'banner_id': banner_id, 'company_info': company_details, 'products': products,
               'categories': product_category,
               'current_user': current_user, 'selected_category': selected_category, 'session': 'false',
               'date': set_new_arrival_date, 'recommented_product': recommented_product}

    return render(request, 'index.html', context)


@never_cache
def customer_logout(request):
    request.session.flush()
    return redirect(home)


@never_cache
def add_company_info(request):
    if request.method == 'POST':
        form = company_info(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('successfully uploaded')
    else:
        form = company_info()
    return render(request, 'add_companyInfo.html', {'form': form})


@never_cache
def add_products(request):
    if request.method == 'POST':
        form = add_product_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('successfully uploaded')
    else:
        form = add_product_form()
    return render(request, 'add_product.html', {'form': form})


@never_cache
def admin_register(request):
    return render(request, 'admin_register.html')


@never_cache
def edit_Product(request):
    products = all_products.objects.all()
    if request.method == 'POST':
        product_id = request.POST['product_id']
        global current_product
        current_product = all_products.objects.get(product_id=product_id)
        return render(request, 'edit_one_product.html', {'current_product': current_product})
    return render(request, 'edit_product.html', {'products': products})


@never_cache
def delete_Product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        all_products.objects.get(product_id=product_id).delete()
    return redirect('/admin/edit_product')


@never_cache
def add_categories(request):
    if request.method == 'POST':
        form = add_category(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('successfully uploaded')
    else:
        form = add_category()
    return render(request, 'add_category.html', {'form': form})


@never_cache
def delete_categories(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        Category.objects.get(id=category_id).delete()
        return redirect('/admin/edit_category')


@never_cache
def edit_categories(request):
    available_categories = Category.objects.all()
    return render(request, 'edit_category.html', {'available_categories': available_categories})


@never_cache
def edit_one_categories(request, category_id):
    category_detail = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_img = request.POST.get('category_img')
        category_detail.category_name = category_name
        category_detail.category_img = category_img
        category_detail.save()
        return redirect('/admin/edit_category')

    return render(request, 'edit_one_category.html', {'category_detail': category_detail})


@never_cache
def add_subcategory(request):
    return render(request, 'add_subcategory.html')


@never_cache
def edit_subcategory(request):
    return render(request, 'edit_category.html')


@never_cache
def add_customer(request):
    if request.method == 'POST':
        form = add_customer_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(admin_pannel)
    else:
        form = add_customer_form()
    return render(request, 'add_customer.html', {'form': form})


@never_cache
def edit_customer(request):
    customers = Customer.objects.all()
    if request.method == 'POST':
        customer_email = request.POST['customer']
        global current_customer
        current_customer = Customer.objects.get(customer_email=customer_email)

        return render(request, 'edit_one_customer.html', {'current_customer': current_customer})
    return render(request, 'edit_customer.html', {'customers': customers})


@never_cache
def edit_one_customer(request):
    customers = Customer.objects.all()
    if request.method == 'POST':
        new_customer_email = request.POST['new_customer_email']
        new_customer_phone_number = request.POST['new_customer_phone_number']
        customer_building_id = request.POST['customer_building_id']
        customer_landmark = request.POST['customer_landmark']
        customer_street = request.POST['customer_street']
        customer_city = request.POST['customer_city']
        customer_country = request.POST['customer_country']
        customer_pincode = request.POST['customer_pincode']
        customer_total_buyed = request.POST['customer_total_buyed']
        customer_status = request.POST['customer_status']
        is_admin = request.POST['is_admin']
        current_customer.customer_email = new_customer_email
        current_customer.customer_phone_number = new_customer_phone_number
        current_customer.customer_building_id = customer_building_id
        current_customer.customer_landmark = customer_landmark
        current_customer.customer_street = customer_street
        current_customer.customer_city = customer_city
        current_customer.customer_country = customer_country
        current_customer.customer_pincode = customer_pincode
        current_customer.customer_total_buyed = customer_total_buyed
        current_customer.customer_status = customer_status
        current_customer.is_admin = is_admin
        current_customer.save()
        return redirect(edit_customer)
    return render(request, 'edit_customer.html', {'customers': customers})


@never_cache
def delete_customer(request):
    customers = Customer.objects.all()
    if request.method == 'POST':
        customer_email = request.POST['customer']
        global current_customer
        current_customer = Customer.objects.get(customer_email=customer_email).delete()
        return render(request, 'edit_customer.html', {'customers': customers})
    return render(request, 'delete_customer.html', {'customers': customers})


@never_cache
def add_banners(request):
    if request.method == 'POST':
        form = add_banner(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('successfully uploaded')
    else:
        form = add_banner()
    return render(request, 'add_banner.html', {'form': form})


@never_cache
def delete_banner(request):
    return render(request, 'delete_banner.html')


@never_cache
def success():
    return HttpResponse('successfully uploaded')


@never_cache
def user_otp_signin(request):
    global customer
    if request.method == 'POST':
        signin_phone_number = request.POST.get('signin_phone_number')
        try:
            current_user = Customer.objects.get(customer_phone_number=signin_phone_number)
            if current_user is not None:
                print('user with this number exist, sending otp')
                # /////////////////////////////////  sending otp    //////////////////////////////////
                try:
                    account_sid = 'ACd9fe7f948f2b0de94a1502c2998c884e'
                    auth_token = '452e06c4f82769e1cf398a2dbbce3f09'
                    client = Client(account_sid, auth_token)
                    global otp
                    otp = str(random.randrange(1000, 9000))
                    message = client.messages \
                        .create(
                        body=f"hi {current_user.customer_email}, Welcome to WideCity Shopping.  Please verify your Phone number with the otp : {otp} , Do to share this number to anyone.",
                        from_='+18304980732',
                        to='+919946658045'
                    )
                    # print(message.sid), {'otp': otp}
                    return render(request, 'verify_otp.html', {'current_user': current_user})
                except:
                    return HttpResponse('no internet')
            else:
                return HttpResponse("sry no user found")
        except:
            return HttpResponse("sry no user found")

    return render(request, 'user_otp_signin.html')


@never_cache
def admin_pannel(request):
    return render(request, 'admin_panel.html')


@never_cache
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        all_users = Customer.objects.all()
        for user in all_users:
            # print(user.customer_email)
            # print(username)
            if user.customer_email == username:
                if user.customer_password == password:
                    if user.is_admin == 'admin':
                        if user.customer_status == 'active':
                            return render(request, 'admin_panel.html')
                        return render(request, 'admin_login.html', {'err': 'The user is Blocked'})
                    return render(request, 'admin_login.html', {'err': 'The user is not an Admin'})
                return render(request, 'admin_login.html', {'err': 'Wrong Password'})
        return render(request, 'admin_login.html', {'err': 'Wrong Email'})
    return render(request, 'admin_login.html', {'err': ''})


@never_cache
def edit_one_product(request):
    products = all_products.objects.all()
    if request.method == 'POST':
        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_category = request.POST['product_category']
        product_subcategory = request.POST['product_subcategory']
        product_description = request.POST['product_description']
        product_gender = request.POST['product_gender']
        product_specification_1 = request.POST['product_specification_1']
        product_specification_2 = request.POST['product_specification_2']
        product_stock_available = request.POST['product_stock_available']
        product_rating = request.POST['product_rating']
        product_total_sold = request.POST['product_total_sold']
        product_review_id = request.POST['product_review_id']
        product_status = request.POST['product_status']
        global current_product
        current_product.product_name = product_name
        current_product.product_price = product_price
        current_product.product_category = product_category
        current_product.product_subcategory = product_subcategory
        current_product.product_description = product_description
        current_product.product_gender = product_gender
        current_product.product_specification_1 = product_specification_1
        current_product.product_specification_2 = product_specification_2
        current_product.product_stock_available = product_stock_available
        current_product.product_rating = product_rating
        current_product.product_total_sold = product_total_sold
        current_product.product_review_id = product_review_id
        current_product.product_status = product_status
        current_product.save()
        return render(request, 'edit_product.html', {'products': products})
    return render(request, 'edit_product.html', {'products': products})


@never_cache
def verify_otp(request, current_user_email):
    if request.method == 'POST':
        otp_1 = str(request.POST['otp_1'])
        otp_2 = str(request.POST['otp_2'])
        otp_3 = str(request.POST['otp_3'])
        otp_4 = str(request.POST['otp_4'])
        entered_otp = otp_1 + otp_2 + otp_3 + otp_4
        print(entered_otp)
        if entered_otp == otp:
            url = '/home/{}'.format(current_user_email)
            return redirect(url)
    return render(request, 'verify_otp.html', {'err': 'Please Enter the valid OTP'})


@never_cache
def product_detail(request, product_id):
    product = all_products.objects.get(product_id=product_id)

    if 'user' in request.session:
        current_user = request.session['user']
        customer = Customer.objects.get(customer_email=current_user)
        context = {'product': product, 'customer': customer}
    else:
        context = {'product': product}

    return render(request, 'product_detail.html', context)


def redirect_home(request):
    return redirect('/home')


def category_products(request, category_name):
    global selected_category
    selected_category = category_name
    return redirect(home)


def add_to_cart(request, product_id):
    current_user = 'guest'
    if 'user' in request.session:
        current_user = request.session['user']

    current_customer = Customer.objects.get(customer_email=current_user)

    all_cart_products = Cart.objects.filter(bag_customer_id=current_customer.id)
    for product in all_cart_products:
        print(product.bag_product_id, product_id)
        if str(product_id) == str(product.bag_product_id):
            product.bag_quantity = int(product.bag_quantity) + 1
            product.save()
            print(product.bag_quantity)
            return redirect(f'/product_detail/{product_id}')

    # works on add cart
    current_product = all_products.objects.get(product_id=int(product_id))
    add_to_cart = Cart.objects.create(bag_customer_id=current_customer.id, bag_product_id=product_id,
                                      bag_quantity=1,
                                      total_price=current_product.product_price)
    add_to_cart.save()
    return redirect(f'/product_detail/{product_id}')


def checkout(request):
    current_user = 'guest'
    sub_total = 0
    if 'user' in request.session:
        current_user = request.session['user']
        sub_total = request.session['subtotal']

    customer = Customer.objects.get(customer_email=current_user)

    current_customer = Customer.objects.get(id=customer.id)
    products = Cart.objects.filter(bag_customer_id=customer.id)
    current_customer_address_count = Address.objects.filter(customer_email=current_user).count()
    current_customer_address = Address.objects.filter(customer_email=current_user)

    context = {'current_user': current_customer, 'address': current_customer_address,
               'address_count': current_customer_address_count, 'sub_total': sub_total}

    return render(request, 'checkout.html', context)


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('signin_email')
        password = request.POST.get('signin_password')
        customers = Customer.objects.all()
        for customer in customers:
            # print(customer.customer_email)
            # print(username)
            if str(customer.customer_email) == str(username):
                request.session['user'] = username
                # url = '/home/{}'.format(customer.customer_email)
                return redirect(home)
    return render(request, 'signin.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('register_email')
        password = request.POST.get('register_password')
        register_phone_number = request.POST.get('register_phone_number')
        new_user = Customer.objects.create(customer_email=username, customer_password=password,
                                           customer_phone_number=register_phone_number)
        new_user.save()
        return HttpResponse('user registered')
    return render(request, 'register.html')


def update_cart(request):
    cart_total = 0

    if request.method == 'POST':
        # we get these datas from the ajax request
        quantity = request.POST.get("Quantity")
        bag_id = request.POST.get("BagId")
        customer_id = request.POST.get("customer_id")

        # take the necessary data from the database using the data in the above variables

        clicked_product_cart_detail = Cart.objects.get(bag_id=bag_id)
        # this variable contains the cart details of the clicked product

        clicked_product_details = all_products.objects.get(product_id=clicked_product_cart_detail.bag_product_id)
        # this variable contains all the details of the clicked product.

        current_customer = Customer.objects.get(id=customer_id)

        # updating the total price in the cart according to the quantity
        price = clicked_product_details.product_price
        total = int(quantity) * int(price)
        clicked_product_cart_detail.total_price = total

        # assigning the new quantity to the database
        clicked_product_cart_detail.bag_quantity = quantity

        # save the updates to the cart in the database
        clicked_product_cart_detail.save()

        cart_products = Cart.objects.filter(bag_customer_id=customer_id)
        for products in cart_products:
            cart_total = cart_total + products.total_price
        sub_total = cart_total
        # if 'user' in request.session == current_customer.customer_email:
        request.session['subtotal'] = sub_total
        # print(request.session['subtotal'])
        return JsonResponse({'total': total, 'quantity': quantity, 'sub_total': sub_total})


def account(request):
    current_user = 'guest'
    if 'user' in request.session:
        current_user = request.session['user']

    customer = Customer.objects.get(customer_email=current_user)
    print('customer_id', customer)
    my_ordered_product_details = Orders.objects.filter(order_customer_id=customer.id)
    product_image_src = all_products.objects.all()
    context = {'my_ordered_product_details': my_ordered_product_details, 'customer': customer,
               'product_image_src': product_image_src}

    return render(request, "account.html", context)


def load_data_in_cart(request):
    if request.method == 'POST':
        bag_id = request.POST.get("BagId")
        customer_id = request.POST.get("CustomerId")
        cart_product = Cart.objects.get(bag_id=bag_id)
        quantity = cart_product.bag_quantity
        print(bag_id)
        # # return HttpResponse('cool got bag id as {} and quantity as {}'.format(bag_id,current_quantity))
        # return redirect('/cart/{}/0'.format(customer_id))
        return JsonResponse({'bag_id': bag_id, 'quantity': quantity, 'customer_id': customer_id})


def item_delete(request):
    if request.method == 'POST':
        bag_id = request.POST.get('bag_id')
        print('bag_id', bag_id)
        cart_product = Cart.objects.get(bag_id=bag_id).delete()
        return JsonResponse({'response': 'success'})

    return redirect('/view_cart')


def place_order(request, customer_id):
    if request.method == 'POST':
        cart_products = Cart.objects.filter(bag_customer_id=customer_id)
        for each_product in cart_products:
            order = Orders.objects.create(order_customer_id=customer_id, order_product_id=each_product.bag_id,
                                          order_quantity=each_product.bag_quantity,
                                          order_total_price=each_product.total_price,
                                          order_ordered_time='23-05-2022', order_expected_time='25-05-2022')
            order.save()
        return redirect('/')


def view_edit_orders(request):
    orders = Orders.objects.all()
    return render(request, 'view_edit_orders.html', {'orders': orders})


def view_cart(request):
    current_user = 'guest'
    if 'user' in request.session:
        current_user = request.session['user']
        customer = Customer.objects.get(customer_email=current_user)
        current_user_cart = Cart.objects.filter(bag_customer_id=customer.id)
        product = all_products.objects.all()
        context = {'current_user_cart': current_user_cart, 'product': product, 'customer': customer}

        return render(request, 'cart.html', context)

    return redirect(signin)


def add_address(request):
    if request.method == 'POST':
        customer_first_name = request.POST.get('customer_first_name')
        customer_last_name = request.POST.get('customer_last_name')
        customer_building_id = request.POST.get('customer_building_id')
        customer_landmark = request.POST.get('customer_landmark')
        customer_street = request.POST.get('customer_street')
        customer_city = request.POST.get('customer_city')
        customer_country = request.POST.get('customer_country')
        customer_pincode = request.POST.get('customer_pincode')
        # customer_phone_number = request.POST.get('customer_phone_number')
        customer_email = request.POST.get('customer_email')

        my_new_address = Address.objects.create(customer_first_name=customer_first_name,
                                                customer_last_name=customer_last_name,
                                                customer_building_id=customer_building_id,
                                                customer_landmark=customer_landmark,
                                                customer_street=customer_street,
                                                customer_city=customer_city,
                                                customer_country=customer_country,
                                                customer_pincode=customer_pincode,
                                                customer_email=customer_email)

        my_new_address.save()
        return redirect(checkout)

    return render(request, 'add_address.html')


def order_request(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        if 'user' in request.session:
            customer_email = request.session['user']
            customer = Customer.objects.get(customer_email=customer_email)
            cart_products = Cart.objects.filter(bag_customer_id=customer.id)
            for product in cart_products:
                new_order = Orders.objects.create(order_customer_id=customer.id,
                                                  order_product_id=product.bag_product_id,
                                                  order_quantity=product.bag_quantity,
                                                  order_total_price=product.total_price,
                                                  order_ordered_time='2022-09-30',
                                                  order_expected_time='2022-09-30',
                                                  order_delivery_status='on the way')
                new_order.save()
                delete = cart_products.delete()

                print(product.bag_product_id)
                success = 'placed successfully'
                return JsonResponse({'order': success})
        return HttpResponse('its your temporary response')


def thankyou_for_order(request):
    return render(request,'thank_you_for_placing_order.html')


def category_view(request, category_id):
    category_ids = Category.objects.all()
    for ids in category_ids:
        if str(category_id) == str(ids.id):
            category_details = Category.objects.get(id=category_id)
            print('category', category_details.category_name)
            products_in_this_category = all_products.objects.filter(product_category=category_details.category_name)
            for product in products_in_this_category:
                print(product.product_name)
            return render(request, 'category_view.html',
                          {'category_details': category_details, 'products': products_in_this_category})


def list_subcategory(request):
    sub_categories = Subcategory.objects.all()
    if request.method == 'POST':

        operation = request.POST.get('operation')
        selected_id = request.POST.get('selected')
        subcategory_details = Subcategory.objects.get(id=selected_id)

        print(operation)
        if operation == 'delete':
            return HttpResponse('its delete')

        elif operation == 'update':
            context = {'category_name': subcategory_details.category_name,
                       'sub_category_name': subcategory_details.sub_category_name}
            form = handle_subcategory(initial=context)
            return render(request, 'handle_subcategory.html', {'form': form})

        else:
            return HttpResponse('there are no operation')

    return render(request, 'list_subcategory.html', {'sub_categories': sub_categories})

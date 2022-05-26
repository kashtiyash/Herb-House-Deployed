import email
from re import U
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import Contact, Customer, Seller, Product, Order
import razorpay
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .tokens import generate_token
from django.utils.encoding import force_bytes, force_str

# Create your views here.


client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))


def home(request):
    return render(request, "mainapp/home.html")


def contactus(request):
    if request.method == "GET":
        return render(request, "mainapp/contactus.html")

    if request.method == "POST":
        user_name = request.POST['name']
        user_email_contact = request.POST['email']
        user_message = request.POST['message']
        userdata = Contact(name=user_name, email=user_email_contact, message=user_message)
        userdata.save()

        try:
            subject = "Thank you for contacting us, We will see your request."
            message = " We will see this query of yours :-\n\n " + user_message + " \n\n Regards,\n Herb House Team"
            sender_email = settings.EMAIL_HOST_USER
            to_email = [user_email_contact]
            send_mail(subject, message, "Don't Reply <do_not_reply@domain.com>", to_email, fail_silently=True)

        except Exception:
            messages.info(request, "Email Not Send")
        return redirect('home')

    else:
        messages.error(request, "404-Page Not Found")

        return redirect("/")


def about(request):
    return render(request, "mainapp/about.html")


def loginpage(request):
    return render(request, "mainapp/loginpage.html")


def logoutpage(request):
    logout(request)
    messages.info(request, "You have been successfully Logged out")
    return redirect('home')


def customerlogin(request):
    if request.method == "POST":
        username = request.POST['customerloginusername']
        password = request.POST['customerloginpassword']
        user = authenticate(username=username, password=password)

        try:
            login(request, user)
            messages.success(request, "You have successfully logged in")
        except Exception:
            messages.error(request, "Invalid Credentials")
        return redirect('home')


def customersignup(request):
    if request.method == "POST":
        username = request.POST['customersignupusername']
        first_name = request.POST['customersignupfirstname']
        last_name = request.POST['customersignuplastname']
        email = request.POST['customersignupemail']
        phone = request.POST['customersignupphone']
        password = request.POST['customersignuppassword']

        if User.objects.filter(username=username):
            messages.error(request, "Username is already taken! Please choose another username")
            return redirect("home")

        if User.objects.filter(email=email):
            messages.error(request, "Email Address is already taken! Please enter another Email")
            return redirect("home")

        if len(username) > 20:
            messages.error(request, "Username should not be greater than 10 chars")
            return redirect("home")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect("home")

        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False

            user.save()

        # Email Confirmation
        current_site = get_current_site(request)
        email_subject = "Hello " + user.first_name + "!! Please confirm your email address to Login into Herb House !!"
        message2 = render_to_string("email_confirmation.html", {"name": user.first_name,
                                                                "domain": current_site.domain,
                                                                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                                                                "token": generate_token.make_token(user)

                                                                })

        email = EmailMessage(
            email_subject,
            message2,
            'Dont Reply <do_not_reply@domain.com>',
            [user.email],
        )

        email.fail_silently = True
        email.send()

        userdata = Customer(phone=phone, user=user)
        userdata.save()

        return redirect('home')

    return redirect(request, "home")


def sellerLogin(request):
    if request.method == "POST":
        username = request.POST['sellerloginusername']
        password = request.POST['sellerloginpassword']
        user = authenticate(username=username, password=password)
        print(user)

        try:
            login(request, user)
            messages.success(request, "You have successfully logged in")

        except Exception:
            messages.error(request, " Invalid Credentials ")
        return redirect('home')


def sellerSignup(request):
    if request.method == "POST":
        username = request.POST['sellersignupusername']
        store_name = request.POST['sellerstorename']
        first_name = request.POST['sellersignupfirstname']
        last_name = request.POST['sellersignuplastname']
        email = request.POST['sellersignupemail']
        phone = request.POST['sellersignupphone']
        password = request.POST['sellersignuppassword']

        if User.objects.filter(username=username):
            messages.error(request, "Username is already taken! Please choose another username")
            return redirect("home")

        if User.objects.filter(email=email):
            messages.error(request, "Email Address is already taken! Please enter another Email")
            return redirect("home")

        if len(username) > 20:
            messages.error(request, "Username should not be greater than 10 chars")
            return redirect("home")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect("home")

        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False

            user.save()

            # Email Confirmation
            current_site = get_current_site(request)
            email_subject = "Hello " + user.first_name + "!! Please confirm your email address to Login into Herb House !!"
            message2 = render_to_string("email_confirmation.html", {"name": user.first_name,
                                                                    "domain": current_site.domain,
                                                                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                                                                    "token": generate_token.make_token(user)

                                                                    })

            email = EmailMessage(
                email_subject,
                message2,
                'Dont Reply <do_not_reply@domain.com>',
                [user.email],
            )

            email.fail_silently = True
            email.send()

            userdata = Seller(phone=phone, user=user, store_name=store_name)
            userdata.save()

        return redirect('home')


def manageProducts(request):
    props = Product.objects.filter(store_id=request.user.username)
    return render(request, 'mainapp/manageproducts.html', {'props': props})


def addProduct(request):
    if request.method == 'POST':
        name = request.POST['productname']
        price = request.POST['productprice']
        quantity = request.POST['productquantity']
        product_id = request.POST['productid']
        description = request.POST['productdescription']
        image = request.FILES.get('product_image2')

        store_id = request.user.username

        productdata = Product(name=name, price=price, quantity=quantity,
                              product_id=product_id, description=description,
                              store_id=store_id, product_image=image)

        productdata.save()
        return redirect('/manageproducts')


def delProduct(request):
    if request.method == 'POST':
        del_prodID = request.POST['productid']
        delete_prod = Product.objects.get(product_id=del_prodID)
        delete_prod.delete()
        props = Product.objects.filter(store_id=request.user.username)
        return redirect('/manageproducts')


def updateProduct(request):
    if request.method == 'POST':
        product_id = request.POST['productid']
        product_name = request.POST['productname']
        quantity = int(request.POST['productquantity'])
        price = request.POST['productprice']
        desc = request.POST['productdescription']

        Product.objects.filter(product_id=product_id).update(name=product_name, price=price, quantity=quantity,
                                                             description=desc)

        return redirect('/manageproducts')


def storeList(request):
    props = Seller.objects.all()
    return render(request, 'mainapp/sellerlist.html', {'props': props})


def productlist(request):
    props = Product.objects.all()
    return render(request, 'mainapp/productlist.html', {'props': props})


# this will show specific products listed by seller

def showStoreProducts(request, username):
    products = Product.objects.filter(store_id=username)
    return render(request, 'mainapp/productlist2.html', {'products': products})


def createOrder(request):
    if request.method == 'POST':
        order_id = len(Order.objects.all()) + 1
        product_id = request.POST['productid']
        store_id = request.POST['storeid']
        customer_id = request.user.username
        email = request.POST['customeremail']
        phone = request.POST['customerphone']
        quantity = int(request.POST['productquantity'])
        price = request.POST['productprice']
        address = request.POST['customeraddress']

        order_total = int(price) * int(quantity)

        orderdata = Order(order_id=order_id, product_id=product_id, store_id=store_id,
                          customer_id=customer_id, email=email, phone=phone, quantity=quantity, order_total=order_total,
                          address=address, razorpay_amount_total=order_total * 100)

        payment = client.order.create({"amount": order_total * 100, "currency": "INR", 'payment_capture': 1})

        Order.razorpay_order_id = payment['id']

        # print("________________________________")
        # print(payment)
        # print("_____________________________")

        orderdata.save()
        orderdata.save()
        return redirect('home')


def myOrders(request):
    props = Order.objects.filter(customer_id=request.user.username)
    pro = Order.order_total

    # for getting total cart amount in rupees
    sum = 0
    for e in Order.objects.filter(customer_id=request.user.username):
        sum += e.order_total

    # for getting total value in paise as razorpay does transaction in paise
    total = 0
    for a in Order.objects.filter(customer_id=request.user.username):
        total += a.razorpay_amount_total

    return render(request, 'mainapp/orderlist.html', {'props': props, "amount": sum, "r_total": total})


def cancelOrder(request):
    if request.method == 'POST':
        cancel_orderID = request.POST['orderid']
        cancel_orderID = int(cancel_orderID)
        cancel_order = Order.objects.get(order_id=cancel_orderID)
        cancel_order.delete()
        props = Order.objects.filter(customer_id=request.user.username)
        return redirect('myOrders')


def manageOrders(request):
    props = Order.objects.filter(store_id=request.user.username)
    return render(request, 'mainapp/manageOrders.html', {'props': props})


def confirmOrder(request):
    if request.method == 'POST':
        del_prodID = request.POST['productid']
        delete_prod = Product.objects.get(product_id=del_prodID)
        delete_prod.delete()
        props = Product.objects.filter(store_id=request.user.username)
        return redirect('/manageorders')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("home")
    else:
        return render(request, "Activation_failed.html")

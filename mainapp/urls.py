from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    # Home
    path('', views.home, name="home"),
    path('contact/', views.contactus, name="contactUs"),
    path("about/", views.about, name="aboutUs"),
    path("login/", views.loginpage, name="loginpage"),
    path("login/customerlogin", views.customerlogin, name="customerlogin"),
    path("login/customersignup", views.customersignup, name="customerSignup"),
    path("login/sellerlogin", views.sellerLogin, name="sellerlogin"),
    path("login/sellersignup", views.sellerSignup, name="sellerSignup"),
    path("logout/", views.logoutpage, name="logout"),

    #CRUD on Products

    path("manageproducts/", views.manageProducts, name="manageProducts"),
    path("manageproducts/addproduct", views.addProduct, name="addProduct"),
    path("manageproducts/delproduct", views.delProduct, name="delProduct"),
    path("manageproducts/updateproduct", views.updateProduct, name="updateProduct"),

    #Store and Product List
    path("storelist/", views.storeList, name="storeList"),
    path("productlist/", views.productlist, name="productList"),
    path("storelist/order", views.createOrder, name="createOrder"),
    path("storelist/<username>", views.showStoreProducts, name="showStoreProducts"),

    #Customer Side
    path("myorders/", views.myOrders, name="myOrders"),
    path("myorders/cancelorder", views.cancelOrder, name="cancelOrder"),

    #Seller Side
    path("manageorders/", views.manageOrders, name="manageOrders"),
    path("manageorders/confirmorder", views.confirmOrder, name="confirmOrder"),
    path("manageorders/cancelorder", views.cancelOrder, name="cancelOrder"),

    path("activate/<uidb64>/<token>", views.activate, name="activate"),

]

# This is just for demo purpose addition
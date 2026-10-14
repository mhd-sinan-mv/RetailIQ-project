"""
URL configuration for RetailIQ project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from turtle import home

from django.contrib import admin
from django.urls import path

from RetailIQApp.views import *
urlpatterns = [
    path('',LoginPage.as_view(),name='LoginPage'),

    # ////////////////////////////////////// ADMIN /////////////////////////////////////
    path('admin_home',admin_home.as_view(),name='admin_home'),
    path('BlockOrUnblockShops',BlockOrUnblockShops.as_view(),name='BlockOrUnblockShops'),
    path('ViewAndVerifyShops',ViewAndVerifyShops.as_view(),name='ViewAndVerifyShops'),
    path('ViewComplaintsAndReply',ViewComplaintsAndReply.as_view(),name='ViewComplaintsAndReply'),
    path('ViewRatingAndFeedback',ViewRatingAndFeedback.as_view(),name='ViewRatingAndFeedback'),

    # //////////////////////////////////// SHOP ////////////////////////////////////////

    path('shop_home',shop_home.as_view(),name='shop_home'),
    path('AddProducts',AddProducts.as_view(),name='AddProducts'),
    path('AddStaff',AddStaff.as_view(),name='AddStaff'),
    path('ManageDiscounts',ManageDiscounts.as_view(),name='ManageDiscounts'),
    path('ManageNotifications',ManageNotifications.as_view(),name='ManageNotifications'),
    path('ManageOffers',ManageOffers.as_view(),name='ManageOffers'),
    path('ManageProducts',ManageProducts.as_view(),name='ManageProducts'),
    path('ManageStaff',ManageStaff.as_view(),name='ManageStaff'),
    path('Register',Register.as_view(),name='Register'),
    path('ViewCustomers',ViewCustomers.as_view(),name='ViewCustomers'),
    path('ViewOrders',ViewOrders.as_view(),name='ViewOrders'),
    path('ViewSales',ViewSales.as_view(),name='ViewSales'),
    path('ViewStockandUpdateStock',ViewStockandUpdateStock.as_view(),name='ViewStockandUpdateStock'),
    path('RatingAndFeedback',RatingAndFeedback.as_view(),name='ratingAndFeedback'),

    #/////////////////////////////////// STAFF ////////////////////////////////////
    path('staff_home',staff_home.as_view(),name='staff_home'),
    path('OrdersAndBill',OrdersAndBill.as_view(),name='OrdersAndBill'),
    path('ViewDiscount',ViewDiscount.as_view(),name='ViewDiscount'),
    path('ViewLowStock',ViewLowStock.as_view(),name='ViewLowStock'),
    path('ViewNotification',ViewNotification.as_view(),name='ViewNotification'),
    path('ViewOffers',ViewOffers.as_view(),name='ViewOffers'),
    path('ViewOrders',ViewOrders.as_view(),name='ViewOrders'),
    path('ViewProducts',ViewProducts.as_view(),name='ViewProducts'),
              
    








    



    
    






    
]

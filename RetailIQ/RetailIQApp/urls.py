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
    path('sendReply/<int:c_id>',sendReply.as_view(),name='sendReply'),
    path('ViewRatingAndFeedback',ViewRatingAndFeedback.as_view(),name='ViewRatingAndFeedback'),
    path('BlockShop/<int:l_id>',BlockShop.as_view(),name='BlockShop'),
    path('UnblockShop/<int:l_id>',UnblockShop.as_view(),name='UnblockShop'),
    path('acceptShop/<int:l_id>',acceptShop.as_view(),name='acceptShop'),
    path('rejectShop/<int:l_id>',rejectShop.as_view(),name='rejectShop'),

    # //////////////////////////////////// SHOP ////////////////////////////////////////

    path('shop_home',shop_home.as_view(),name='shop_home'),
    path('AddProducts',AddProducts.as_view(),name='AddProducts'),
    path('AddStaff',AddStaff.as_view(),name='AddStaff'),
    path('AddDiscounts',addDiscounts.as_view(),name='addDiscounts'),
    path('ManageDiscounts',ManageDiscounts.as_view(),name='ManageDiscounts'),
    path('ViewNotificationsShop',viewNotificationsShop.as_view(),name='ViewNotificationsShop'),
    path('ManageOffers',ManageOffers.as_view(),name='ManageOffers'),
    path('editOffer/<int:o_id>',editOffer.as_view(),name='editOffer'),
    path('deleteOffer/<int:o_id>',deleteOffer.as_view(),name='deleteOffer'),
    path('ManageProducts',ManageProducts.as_view(),name='ManageProducts'),
    path('enableProduct/<int:p_id>',enableProduct.as_view(),name='enableProduct'),
    path('disableProduct/<int:p_id>',disableProduct.as_view(),name='disableProduct'),
    path('editProduct/<int:p_id>',editProduct.as_view(),name='editProduct'),
    path('deleteProduct/<int:p_id>',deleteProduct.as_view(),name='deleteProduct'),
    path('ManageStaff',ManageStaff.as_view(),name='ManageStaff'),
    path('Register',RegisterUser.as_view(),name='Register'),
    path('ViewCustomers',ViewCustomers.as_view(),name='ViewCustomers'),
    path('ViewSales',ViewSales.as_view(),name='ViewSales'),
    path('ViewStockandUpdateStock',ViewStockandUpdateStock.as_view(),name='ViewStockandUpdateStock'),
    path('RatingAndFeedback',RatingAndFeedback.as_view(),name='ratingAndFeedback'),
    path('addManageCategories',addManageCategories.as_view(),name='addManageCategories'),
    path('complaints',complaints.as_view(),name="complaints"),
    path('startDiscount/<int:d_id>',startDiscount.as_view(),name='startDiscount'),
    path('stopDiscount/<int:d_id>',stopDiscount.as_view(),name='stopDiscount'),


    #/////////////////////////////////// STAFF ////////////////////////////////////
    path('staff_home',staff_home.as_view(),name='staff_home'),
    path('OrdersAndBill',OrdersAndBill.as_view(),name='OrdersAndBill'),
    path('ViewDiscount',ViewDiscount.as_view(),name='ViewDiscount'),
    path('ViewLowStock',ViewLowStock.as_view(),name='ViewLowStock'),
    path('ViewOffers',ViewOffers.as_view(),name='ViewOffers'),
    path('ViewOrders',ViewOrders.as_view(),name='ViewOrders'),    #   moved from shop
    path('ViewProducts',ViewProducts.as_view(),name='ViewProducts'),
    path('ViewNotifications',viewNotifications.as_view(),name='ViewNotifications'),
              
    








    



    
    






    
]

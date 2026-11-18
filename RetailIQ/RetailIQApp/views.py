from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from RetailIQApp.form import *
from RetailIQApp.models import *

import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta# Create your views here.

class LoginPage(View):
    def get(self,request):
        return render(request,'Login.html')
    
    def post(self,request):
        try:
            username1=request.POST['username']
            password1=request.POST['password']
            print(username1)
            print(password1)

            login_obj=LoginTable.objects.get(login_identifier=username1,password=password1)
            print("$$$$$$$$$$$$$$$$$$$",login_obj)
            request.session['loginid']=login_obj.id
            # global staff_id #declares staff login as global to access without declaring everytime
            # staff_id= StaffTable.objects.get(LOGINID_id=request.session['loginid'])
            print(request.session['loginid'])

            if login_obj.user_type=="admin":
                return HttpResponse('''<script>alert("admin_home");window.location=("admin_home")</script>''')
            elif login_obj.user_type=="shop":
                return HttpResponse('''<script>alert("shop_home");window.location=("shop_home")</script>''')
            elif login_obj.user_type=="staff":
                return HttpResponse('''<script>alert("staff_home");window.location=("staff_home")</script>''')
            else:
                return HttpResponse('''<script>alert("no_user_found");window.location=("/")</script>''')
        except LoginTable.DoesNotExist:
            return HttpResponse('''<script>alert("invalid_credentials");window.location=("/")</script>''')



# //////////////////////////////////////////// ADMIN /////////////////////////////////////

class admin_home(View):
    def get(self,request):
        return render(request,'admin/admin_home.html')
    
class BlockOrUnblockShops(View):
    def get(self,request):
        obj = ShopTable.objects.all()
        return render(request,'admin/BlockOrUnblockShops.html', {'shop_data':obj})

class BlockShop(View):
    def get(self,request,l_id):
        obj = LoginTable.objects.get(id=l_id)
        obj.user_type = "Blocked"
        obj.save()
        return HttpResponse('''<script>alert("Shop Blocked");window.location=("/BlockOrUnblockShops")</script>''')

class UnblockShop(View):
    def get(self,request,l_id):
        obj = LoginTable.objects.get(id = l_id)
        obj.user_type = "shop"
        obj.save()
        return HttpResponse('''<script>alert("shop unblocked");window.location=("/BlockOrUnblockShops")</script>''')


class ViewAndVerifyShops(View):
    def get(self,request):
        obj = ShopTable.objects.all()
        return render(request,'admin/ViewAndVerifyShops.html', {'shop_data':obj})

class acceptShop(View):
    def get(self,request,l_id):
        obj = LoginTable.objects.get(id = l_id)
        obj.user_type = 'shop'
        obj.save()
        return HttpResponse('''<script>alert("Shop Verified");window.location=("/ViewAndVerifyShops")</script>''')

class rejectShop(View):
    def get(self,request,l_id):
        obj = LoginTable.objects.get(id = l_id)
        obj.user_type = 'shopRejected'
        obj.save()
        return HttpResponse('''<script>alert("Shop rejected");window.location=("/ViewAndVerifyShops")</script>''')


class ViewComplaintsAndReply(View):
    def get(self,request):
        obj = ComplaintTable.objects.all()
        return render(request,'admin/ViewComplaintsAndReply.html', {'complaint_data':obj})
    # def post(self,request):
    #     form = ComplaintForm(request.POST)
    #     if form.is_valid():
    #         f = form.save(commit=False)
    #         f.SHOPID = ShopTable.objects.get(LOGINID_id= request.session['loginid'])
    #         f.save()
    #         return HttpResponse('''<script>alert("Reply sent back");window.location=("admin_home")</script>''')

class sendReply(View):
    def post(self,request,c_id):
        obj = ComplaintTable.objects.get(id=c_id)
        obj.reply = request.POST['reply']
        obj.reply_date = datetime.now()
        obj.save()
        return HttpResponse('''<script>alert("Reply sent back");window.location=("/ViewComplaintsAndReply")</script>''')


    

    
class ViewRatingAndFeedback(View):
    def get(self,request):
        obj = FeedbackTable.objects.all()
        return render(request,'admin/ViewRatingAndFeedback.html', {'feedback_data':obj})   
  
    #///////////////////////////// SHOP //////////////////////////////////

class shop_home(View):
    def get(self,request):
        return render(request,'shop/shop_home.html')


class AddProducts(View):
    def get(self,request):
        obj = CategoryTable.objects.filter(SHOPID__LOGINID__id=request.session['loginid']) #newly added 
        return render(request,'shop/AddProducts.html',{'categories':obj})
    
    def post(self,request):
        form = ProductForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.SHOPID=ShopTable.objects.get(LOGINID_id= request.session['loginid'])
            f.CATEGORY = CategoryTable.objects.get(id = request.POST.get('category_name')) #newly added 
            f.STOCK = StockTable.objects.create(quantity = request.POST['quantity']) #newly added 
            f.save()
            return HttpResponse('''<script>alert("product added successfully");window.location=("shop_home")</script>''')

class AddStaff(View):
    def get(self,request):
        return render(request,'shop/AddStaff.html')   
    
    def post(self, request):
        form = StaffForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.LOGINID=LoginTable.objects.create(login_identifier=request.POST['staff_code'], password=request.POST['assigned_password'], user_type='staff')
            f.SHOPID=ShopTable.objects.get(LOGINID_id= request.session['loginid'])
            f.save()
            return HttpResponse('''<script>alert("staff registered successfully");window.location=("shop_home")</script>''')

class addDiscounts(View): #newly added
    def get(self,request):
        obj = ProductTable.objects.filter(SHOPID__LOGINID__id=request.session['loginid']) 
        return render(request,'shop/AddDiscounts.html',{'products':obj})
    
    def post(self,request):
        form = DiscountForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            # f.SHOPID=ShopTable.objects.get(LOGINID_id= request.session['loginid']) 
            f.PRODUCT = ProductTable.objects.get(id = request.POST.get('product_name'),SHOPID__LOGINID_id= request.session['loginid']) #confirm this line is correct or not
            f.save()
            return HttpResponse('''<script>alert("discount added successfully");window.location=("shop_home")</script>''')

class ManageDiscounts(View):
    def get(self,request):
        obj = DiscountTable.objects.select_related('PRODUCT').filter(PRODUCT__SHOPID__LOGINID_id=request.session['loginid'])
        return render(request,'shop/manageDiscounts.html', {'discount_data':obj})

class startDiscount(View):
    def get(self,request,d_id):
        obj = DiscountTable.objects.get(id=d_id)
        obj.status='Enable'
        obj.save()
        return HttpResponse('''<script>alert("discount enabled successfully");window.location=("/ManageDiscounts")</script>''')

class stopDiscount(View):
    def get(self,request,d_id):
        obj = DiscountTable.objects.get(id=d_id)
        obj.status = 'Disable'
        obj.save()
        return HttpResponse('''<script>alert("discount disabled successfully");window.location=("/ManageDiscounts")</script>''')


class viewNotificationsShop(View):
    def get(self,request):
        obj = NotificationTable.objects.select_related('PRODUCT').filter(PRODUCT__SHOPID__LOGINID_id=request.session['loginid'])
        return render(request,'shop/viewNotificationsShop.html', {'notification_data':obj})

class ManageOffers(View): 
    def get(self,request):
        obj = OfferTable.objects.filter(SHOPID__LOGINID_id=request.session['loginid']).all()
        return render(request,'shop/ManageOffers.html', {'offer_data':obj})

    def post(self,request): #newly added
        form = OfferForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.SHOPID = ShopTable.objects.get(LOGINID_id= request.session['loginid']) 
            f.save()
            return HttpResponse('''<script>alert("offer added successfully");window.location=("ManageOffers")</script>''')

class editOffer(View):
    def get(self,request,o_id):
        obj = OfferTable.objects.get(id=o_id)
        start_date = str(obj.offer_start_date)
        end_date = str(obj.offer_end_date)
        return render(request,'shop/edit/editOffer.html',{'editOffer':obj, 'startDate':start_date, 'endDate':end_date})
    def post(self,request,o_id):
        obj = OfferTable.objects.get(id=o_id)
        form = OfferEditForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert("offer edit successfully");window.location=("/ManageOffers")</script>''')

class deleteOffer(View):
    def get(self,request,o_id):
        obj = OfferTable.objects.get(id=o_id)
        obj.delete()
        return HttpResponse('''<script>alert("offer delete successfully");window.location=("/ManageOffers")</script>''')
    
class ManageProducts(View):
    def get(self,request):
        obj = ProductTable.objects.select_related('CATEGORY','STOCK').filter(SHOPID__LOGINID_id=request.session['loginid'])
        return render(request,'shop/ManageProducts.html', {'product_data':obj}) 

class enableProduct(View):
    def get(self,request,p_id):
        obj = ProductTable.objects.get(id=p_id)
        obj.status='Enable'
        obj.save()
        return HttpResponse('''<script>alert("product enabled successfully");window.location=("/ManageProducts")</script>''')

class disableProduct(View):
    def get(self,request,p_id):
        obj = ProductTable.objects.get(id=p_id)
        obj.status='Disable'
        obj.save()
        return HttpResponse('''<script>alert("product disabled successfully");window.location=("/ManageProducts")</script>''')

class editProduct(View):
    def get(self,request,p_id):
        obj = ProductTable.objects.get(id=p_id)
        cat_obj = CategoryTable.objects.all()
        manufacturing_date = str(obj.manufacturing_date)
        expiry_date = str(obj.expiry_date)
        return render(request,'shop/edit/editProduct.html',{'editProduct':obj, 'manufacturing_date':manufacturing_date, 'expiry_date':expiry_date, 'category':cat_obj})
    
    def post(self,request,p_id):
        obj = ProductTable.objects.get(id=p_id)
        form = ProductEditForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert("product edit successfully");window.location=("/ManageProducts")</script>''')

class deleteProduct(View):
    def get(self,request,p_id):
        obj = ProductTable.objects.get(id=p_id)
        obj.delete()
        return HttpResponse('''<script>alert("product delete successfully");window.location=("/ManageProducts")</script>''')
    
class addManageCategories(View): #newly added
    def get(self,request):
        obj = CategoryTable.objects.filter(SHOPID__LOGINID_id=request.session['loginid'])
        return render(request,'shop/addManageCategories.html', {'categories':obj})
    def post(self,request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.SHOPID = ShopTable.objects.get(LOGINID_id= request.session['loginid']) 
            f.save()
            return HttpResponse('''<script>alert("Category added successfully");window.location=("addManageCategories")</script>''')

class editCategories(View):
    def get(self,request,cat_id):
        obj = CategoryTable.objects.get(id=cat_id)
        return render(request,'shop/edit/editCategories.html',{'editCategories':obj})
    def post(self,request,cat_id):
        obj = CategoryTable.objects.get(id=cat_id)
        form = categoryEditForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert("category edit successful");window.location=("/addManageCategories")</script>''')

class deleteCategories(View):
    def get(self,request,cat_id):
        obj = CategoryTable.objects.get(id=cat_id)
        obj.delete()
        return HttpResponse('''<script>alert("category delete successfully");window.location=("/addManageCategories")</script>''')

class ManageStaff(View):
    def get(self,request):
        obj = StaffTable.objects.filter(SHOPID__LOGINID_id=request.session['loginid'])
        return render(request,'shop/ManageStaff.html', {'staff_data':obj}) 

class editStaff(View):
    def get(self,request,s_id):
        obj = StaffTable.objects.get(id=s_id)
        return render(request,'shop/edit/editStaff.html',{'editStaff':obj})
    def post(self,request,s_id):
        obj = StaffTable.objects.get(id=s_id)
        login_obj = LoginTable.objects.get(id=obj.LOGINID.id)
        login_obj.password=request.POST['assigned_password']
        login_obj.save()
        form = StaffEditForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert("staff update successful");window.location=("/ManageStaff")</script>''')

class deleteStaff(View):
    def get(self,request,s_id):
        obj = StaffTable.objects.get(id=s_id)
        obj.delete()
        return HttpResponse('''<script>alert("staff delete successfully");window.location=("/ManageStaff")</script>''')


class RegisterUser(View):
    def get(self,request):
        return render(request,'shop/Register.html') 

    def post(self,request):  #confirm whether this creates shop correctly?
        form = ShopForm(request.POST)
        if form.is_valid():
            password=request.POST['password']
            confirmPasword=request.POST['confirmPassword']
            if password == confirmPasword:
                f=form.save(commit=False)  
                f.LOGINID = LoginTable.objects.create(login_identifier=request.POST['email'], password=request.POST['password'], user_type='shopToAccept')
                f.save()
                return HttpResponse('''<script>alert("New user registered successfully");window.location=("/")</script>''')
            else:
                return HttpResponse('''<script>alert("Passwords didn't match");window.location=("Register")</script>''')


class ViewCustomers(View):
    def get(self,request):
        obj = CustomerTable.objects.filter(SHOPID__LOGINID_id=request.session['loginid'])
        return render(request,'shop/ViewCustomers.html', {'customer_data':obj})

class editCustomer(View):
    def get(self,request,cust_id):
        obj = CustomerTable.objects.get(id=cust_id)
        return render(request,'shop/edit/editCustomer.html',{'cust':obj})
    def post(self,request,cust_id):
        obj = CustomerTable.objects.get(id=cust_id)
        form = CustomerEditForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert("customer update successful");window.location=("/ViewCustomers")</script>''')

class deleteCustomer(View):
    def get(self,request,cust_id):
        obj = CustomerTable.objects.get(id=cust_id)
        obj.delete()
        return HttpResponse('''<script>alert("Customer delete successfully");window.location=("/ViewCustomers")</script>''')



class ViewSales(View):
    def get(self,request):
        obj = OrderItemTable.objects.select_related('ORDER','PRODUCT').filter(PRODUCT__SHOPID__LOGINID_id=request.session['loginid']).prefetch_related('PRODUCT__discounttable_set') #here first got inside product table and then reverse relation to discount table
        return render(request,'shop/ViewSales.html', {'order_data':obj}) 

class ViewStockandUpdateStock(View):
    def get(self,request):
        obj = ProductTable.objects.filter(SHOPID__LOGINID_id=request.session['loginid']) #select_related not needed?
        return render(request,'shop/ViewStockandUpdateStock.html', {'stock_data':obj})

class updateStock(View):
    def get(self,request,stock_id):
        obj = StockTable.objects.get(id=stock_id)
        return render(request,'shop/edit/updateStock.html',{'updateStock':obj})
    def post(self,request,stock_id):
        obj = StockTable.objects.get(id=stock_id)
        form = StockEditForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponse('''<script>alert("stock update successful");window.location=("/ViewStockandUpdateStock")</script>''')


class RatingAndFeedback(View):
    def get(self,request):
        return render(request,'shop/RatingAndFeedback.html')
    def post(self,request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.SHOPID = ShopTable.objects.get(LOGINID_id= request.session['loginid']) 
            f.save()
            return HttpResponse('''<script>alert("feedback added successfully");window.location=("shop_home")</script>''')

class complaints(View):
    def get(self,request):
        obj = ComplaintTable.objects.filter(SHOPID__LOGINID__id =request.session['loginid'])
        return render(request,'shop/complaintsViewReply.html',{'compData':obj})
    def post(self,request):
        form = ComplaintForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.SHOPID = ShopTable.objects.get(LOGINID_id= request.session['loginid'])
            f.save()
            return HttpResponse('''<script>alert("Complaint sent to admin successfully");window.location=("shop_home")</script>''')

    
#////////////////////////////// STAFF /////////////////////////////////////

class staff_home(View):
    def get(self,request):
        return render(request,'staff/staff_home.html')

class OrdersAndBill(View):
    def get(self,request):
        return render(request,'staff/OrdersAndBill.html') 
    
class ViewDiscount(View):
    def get(self,request):
        staff_id = StaffTable.objects.get(LOGINID_id=request.session['loginid'])
        shop_id=staff_id.SHOPID
        obj = DiscountTable.objects.select_related('PRODUCT').filter(PRODUCT__SHOPID_id=shop_id)
        return render(request,'staff/ViewDiscount.html', {'discount_data':obj})
    
class ViewLowStock(View):
    def get(self,request):
        staff_id = StaffTable.objects.get(LOGINID_id=request.session['loginid'])
        shop_id = staff_id.SHOPID
        obj1 = ProductTable.objects.filter(SHOPID__id=shop_id.id)
        low_stock_obj = []
        for i in obj1:
            stock=i.STOCK.quantity
            if stock <50:
                low_stock_obj.append(i.id)
        obj = ProductTable.objects.filter(id__in=low_stock_obj)
        return render(request,'staff/ViewLowStock.html', {'stock_data':obj}) #here only products which stocks are low is shown


class viewNotifications(View): #shows blank page
    def get(self,request):
        staff_id = StaffTable.objects.get(LOGINID_id=request.session['loginid'])
        shop_id=staff_id.SHOPID
        obj = NotificationTable.objects.select_related('PRODUCT').filter(PRODUCT__SHOPID_id=shop_id).all()
        return render(request,'staff/ViewNotifications.html',{'notification_data_staff':obj})
        

class ViewOffers(View):
    def get(self,request):
        staff_id = StaffTable.objects.get(LOGINID_id=request.session['loginid'])
        shop_id=staff_id.SHOPID
        obj = OfferTable.objects.filter(SHOPID_id=shop_id)
        return render(request,'staff/ViewOffers.html', {'offer_data':obj})

class ViewProducts(View):
    def get(self, request):
        staff_id = StaffTable.objects.get(LOGINID_id=request.session['loginid'])
        shop_id=staff_id.SHOPID
        obj = ProductTable.objects.select_related('CATEGORY','STOCK').prefetch_related('discounttable_set').filter(SHOPID_id=shop_id)
        return render(request, 'staff/ViewProducts.html', {'product_data_staff': obj })

class ViewOrders(View):
    def get(self,request):
        staff_id = StaffTable.objects.get(LOGINID_id=request.session['loginid'])
        shop_id=staff_id.SHOPID
        obj = OrderItemTable.objects.select_related('ORDER','PRODUCT').filter(PRODUCT__SHOPID_id=shop_id).all()
        return render(request,'staff/ViewOrders.html', {'order_data':obj})

# class ViewProducts(View):
#     def get(self,request):
#         obj = ProductTable.objects.select_related('category','STOCK').all()
#         # obj = ProductTable.objects.select_related('category','quantity','offers','discount').all()
#         return render(request,'staff/ViewProducts.html', {'product_data_staff':obj})
    
class ForgetPassword(View):

    def get(self, request):
        return render(request, 'reset_password/forgot_password.html')

    def post(self, request):

        email = request.POST.get('Email')

        if not email:
            messages.error(request, "Email is required.")
            return redirect('/forgotPassword')

        user_tables = [ShopTable]

        for table in user_tables:
            try:
                user = table.objects.get(email=email)

                # Generate 6-digit OTP
                otp = str(random.randint(100000, 999999))

                # Store OTP in session
                request.session['reset_otp'] = otp
                request.session['reset_email'] = email
                request.session['otp_expiry'] = (
                    timezone.now() + timedelta(minutes=5)
                ).isoformat()

                # Send OTP
                send_mail(
                    'Password Reset OTP',
                    f'Your OTP for password reset is {otp}. '
                    'This OTP is valid for 5 minutes.',
                    '@gmail.com', #email id
                    [email],
                    fail_silently=False,
                )

                return redirect('/VerifyOTP')

            except table.DoesNotExist:
                continue

        messages.error(request, "Email not found.")
        return redirect('/forgotPassword')

class VerifyOTP(View):

    def get(self, request):
        return render(request, 'reset_password/otp_new_pass.html')

    def post(self, request):

        entered_otp = request.POST.get('OTP')

        stored_otp = request.session.get('reset_otp')
        expiry = request.session.get('otp_expiry')

        if not stored_otp or not expiry:
            messages.error(request, "Please request a new OTP.")
            return redirect('/Forgotpassword')

        expiry = timezone.datetime.fromisoformat(expiry)

        if timezone.now() > expiry:
            request.session.flush()
            messages.error(request, "OTP expired. Request a new one.")
            return redirect('/Forgotpassword')

        if entered_otp == stored_otp:

            request.session['otp_verified'] = True
            request.session.pop('reset_otp', None)
            user_tables = [ShopTable]
            
            for table in user_tables:
                try:
                    user = table.objects.get(email=request.session.get('reset_email'))
                    login_obj = LoginTable.objects.get(id=user.LOGINID.id)
                    newPassword = request.POST['newPassword']
                    confirmPassword = request.POST['confirmPassword']
                    if newPassword == confirmPassword:
                        login_obj.password = newPassword
                        login_obj.save()
                        return redirect('/')
                    else:
                     return HttpResponse('''<script>alert("Passwords didn't match");window.location=("/")</script>''')

                except:
                     return HttpResponse('''<script>alert("user not found");window.location=("/")</script>''')

        messages.error(request, "Invalid OTP.")
        return redirect('/VerifyOTP')


# class forgotPassword(View):
#     def get(self,request):
#         return render(request,'reset_password/forgot_password.html')
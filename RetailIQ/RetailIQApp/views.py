from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from RetailIQApp.form import *
from RetailIQApp.models import *

# Create your views here.

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

class ViewAndVerifyShops(View):
    def get(self,request):
        obj = ShopTable.objects.all()
        return render(request,'admin/ViewAndVerifyShops.html', {'shop_data':obj})

class ViewComplaintsAndReply(View):
    def get(self,request):
        obj = ComplaintTable.objects.all()
        return render(request,'admin/ViewComplaintsAndReply.html', {'complaint_data':obj})
    
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
            f.SHOPID=ShopTable.objects.get(LOGINID_id= request.session['loginid']) 
            f.PRODUCT = ProductTable.objects.get(id = request.POST.get('product_name')) 
            f.save()
            return HttpResponse('''<script>alert("discount added successfully");window.location=("shop_home")</script>''')


class ManageDiscounts(View):
    def get(self,request):
        obj = DiscountTable.objects.select_related('PRODUCT').filter(PRODUCT__SHOPID__LOGINID_id=request.session['loginid'])
        return render(request,'shop/manageDiscounts.html', {'discount_data':obj})

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

class ManageProducts(View):
    def get(self,request):
        obj = ProductTable.objects.select_related('CATEGORY','STOCK').filter(SHOPID__LOGINID_id=request.session['loginid'])
        return render(request,'shop/ManageProducts.html', {'product_data':obj}) 

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


class ManageStaff(View):
    def get(self,request):
        obj = StaffTable.objects.filter(SHOPID__LOGINID_id=request.session['loginid'])
        return render(request,'shop/ManageStaff.html', {'staff_data':obj}) 

class Register(View):
    def get(self,request):
        return render(request,'shop/Register.html') 

class ViewCustomers(View):
    def get(self,request):
        obj = CustomerTable.objects.filter(SHOPID__LOGINID_id=request.session['loginid'])
        return render(request,'shop/ViewCustomers.html', {'customer_data':obj})
    
class ViewSales(View):
    def get(self,request):
        obj = OrderItemTable.objects.select_related('ORDER','PRODUCT').filter(PRODUCT__SHOPID__LOGINID_id=request.session['loginid']).prefetch_related('PRODUCT__discounttable_set') #here first got inside product table and then reverse relation to discount table
        return render(request,'shop/ViewSales.html', {'order_data':obj}) 

class ViewStockandUpdateStock(View):
    def get(self,request):
        obj = ProductTable.objects.filter(SHOPID__LOGINID_id=request.session['loginid']) #select_related not needed?
        return render(request,'shop/ViewStockandUpdateStock.html', {'stock_data':obj})

class RatingAndFeedback(View):
    def get(self,request):
        return render(request,'shop/RatingAndFeedback.html')
    
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
    
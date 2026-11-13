from django.forms import ModelForm

from RetailIQApp.models import CategoryTable, ComplaintTable, CustomerTable, DiscountTable, FeedbackTable, NotificationTable, OfferTable, OrderItemTable, OrderTable, ProductTable, ShopTable, StaffTable, StockTable

class StaffForm(ModelForm):
    class Meta():
        model = StaffTable
        fields = ['staff_code', 'name','phone','email','designation','assigned_counter']

class ShopForm(ModelForm):
    class Meta():
        model = ShopTable
        fields = ['shop_name', 'email','phone']

class CategoryForm(ModelForm):
    class Meta():
        model = CategoryTable
        fields = ['category_name', 'category_description','is_active']

class StockForm(ModelForm):
    class Meta():
        model = StockTable
        fields = ['quantity','status',]

class ProductForm(ModelForm):
    class Meta():
        model = ProductTable
        fields = ['product_name', 'brand','expiry_date','manufacturing_date','barcode','purchase_price','selling_price','unit','description','supplier_name','supplier_email','supplier_phone']


class CustomerForm(ModelForm):
    class Meta():
        model = CustomerTable
        fields = ['name', 'phone','email','address',]

class OrderForm(ModelForm):
    class Meta():
        model = OrderTable
        fields = ['bill_number','total_price','discount_amount','final_price','payment_method']

class OrderItemForm(ModelForm):
    class Meta():
        model = OrderItemTable
        fields = ['quantity', 'unit_price','total_price','discount_amount']

class OrderItemForm(ModelForm):
    class Meta():
        model = OfferTable
        fields = ['offer_name', 'offer_description','offer_type','offer_start_date','offer_end_date','is_active']


class DiscountForm(ModelForm):
    class Meta():
        model = DiscountTable
        fields = ['discount_type', 'discount_value','start_date','end_date']


class NotificationForm(ModelForm):
    class Meta():
        model = NotificationTable
        fields = ['notification_title', 'notification_message','is_read']


class ComplaintForm(ModelForm):
    class Meta():
        model = ComplaintTable
        fields = [ 'complaint_description','reply','reply_date']


class FeedbackForm(ModelForm):
    class Meta():
        model = FeedbackTable
        fields = ['feedback_description','rating']
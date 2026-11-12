from django.db import models
from django.utils import timezone

# Create your models here.


class LoginTable(models.Model):
    login_identifier = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=30, null=True, blank=True)  # need to hash passwords
    user_type = models.CharField(max_length=20, null=True, blank=True)
    # implement OneToOneField for efficient login process , in this method multiple shops might have same identifiers (try using django 's inbuilt method for login authentication)

class ShopTable(models.Model):
    shop_name = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    LOGINID = models.ForeignKey(LoginTable, on_delete=models.CASCADE, null=True, blank=True)

class StaffTable(models.Model):
    SHOPID = models.ForeignKey(ShopTable, on_delete=models.CASCADE, null=True, blank=True)
    staff_code = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    designation = models.CharField(max_length=20, null=True, blank=True)
    assigned_counter = models.IntegerField(null=True, blank=True) #can be null if the shop does not have that counter pattern
    LOGINID = models.ForeignKey(LoginTable, on_delete=models.CASCADE, null=True, blank=True)

class CategoryTable(models.Model):
    SHOPID = models.ForeignKey(ShopTable, on_delete=models.PROTECT, null=True, blank=True)
    category_name = models.CharField(max_length=20, null=True, blank=True)
    category_description = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class StockTable(models.Model):
    # fk to and from product table , that might be the reason why quantity is not appearing in viewproducts.html , confirm it and look for reverse relation
    quantity = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, null=True, blank=True)

    # Try Adding a StockTransactionTable for tracking stock movements


class ProductTable(models.Model):
    SHOPID = models.ForeignKey(ShopTable, on_delete=models.PROTECT, null=True, blank=True) #necessary? because there is fk to category table
    CATEGORY = models.ForeignKey(CategoryTable,on_delete=models.PROTECT,null=True,blank=True)
    product_name = models.CharField(max_length=50, null=True, blank=True)
    STOCK = models.ForeignKey(StockTable, on_delete=models.PROTECT, null=True, blank=True) #not appearing in viewproducts.html
    brand = models.CharField(max_length=20, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    manufacturing_date = models.DateField(null=True, blank=True)
    barcode = models.IntegerField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    # discount = models.ForeignKey('DiscountTable', on_delete=models.PROTECT, null=True, blank=True)
    # offers = models.ForeignKey('OfferTable', on_delete=models.PROTECT, null=True, blank=True)
    supplier_name = models.CharField(max_length=20, null=True, blank=True)
    supplier_email = models.EmailField(max_length=50, null=True, blank=True)
    supplier_phone = models.CharField(max_length=20, null=True, blank=True)
    # Try making a seperate SupplierTable for supplier info




class CustomerTable(models.Model):
    SHOPID = models.ForeignKey(ShopTable, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    # OrderItemTable is added along with OrderTable so as the given refernce from chatgpt which said that 
    # OrderTable alone can only store the product_id and quantity of a single product, but if we want to store 
    # multiple products in a single order, we need to create a separate OrderItemTable that will have a foreign key 
    # reference to the OrderTable and will store the product_id and quantity of each product in the order. This way, 
    # we can have multiple OrderItemTable entries for a single OrderTable entry, allowing us to store multiple products in a single order.

class OrderTable(models.Model):
    # fk to shopid removed
    bill_number = models.CharField(max_length=20, null=True, blank=True)
    customer_id = models.ForeignKey(CustomerTable, on_delete=models.SET_NULL, null=True, blank=True) # it is an optional feature, as some customers may not want to provide their details, so we can make it optional
    date_time = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=20, null=True, blank=True)

class OrderItemTable(models.Model):
    ORDER = models.ForeignKey(OrderTable, on_delete=models.PROTECT, null=True, blank=True)
    PRODUCT = models.ForeignKey(ProductTable, on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) #fk to product table's selling price
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class OfferTable(models.Model):
    SHOPID = models.ForeignKey(ShopTable, on_delete=models.CASCADE, null=True, blank=True)
    offer_name = models.CharField(max_length=20, null=True, blank=True)
    offer_description = models.CharField(max_length=100, null=True, blank=True)
    offer_type = models.CharField(max_length=20, null=True, blank=True)
    offer_start_date = models.DateField(null=True, blank=True)
    offer_end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #set reverse relation with product table to display product name

class DiscountTable(models.Model):
    PRODUCT = models.ForeignKey(ProductTable, on_delete=models.CASCADE, null=True, blank=True)
    discount_type = models.CharField(max_length=20, null=True, blank=True)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #set reverse relation with product table to display product name

     
class NotificationTable(models.Model):
    PRODUCT = models.ForeignKey(ProductTable, on_delete=models.CASCADE, null=True, blank=True)
    notification_title = models.CharField(max_length=20, null=True, blank=True)
    notification_message = models.CharField(max_length=100, null=True, blank=True)
    notification_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True) it is already there in notification_date field, so no need to add it again

     
class ComplaintTable(models.Model):
    SHOPID = models.ForeignKey(ShopTable, on_delete=models.CASCADE, null=True, blank=True)
    complaint_date = models.DateTimeField(auto_now_add=True)
    complaint_description = models.CharField(max_length=100, null=True, blank=True)
    reply = models.CharField(max_length=100, null=True, blank=True)
    reply_date = models.DateTimeField(null=True, blank=True)


class FeedbackTable(models.Model):
    SHOPID = models.ForeignKey(ShopTable, on_delete=models.CASCADE, null=True, blank=True)
    feedback_date = models.DateTimeField(auto_now_add=True)
    feedback_description = models.CharField(max_length=100, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
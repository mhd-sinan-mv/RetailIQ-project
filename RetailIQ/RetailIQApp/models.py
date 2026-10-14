from django.db import models

# Create your models here.


class LoginTable(models.Model):
    Login_identifier = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=30, null=True, blank=True)
    user_type = models.CharField(max_length=20, null=True, blank=True)

class ShopTable(models.Model):
    shop_name = models.CharField(max_length=40, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    Date_joined = models.DateField(auto_now_add=True)
    Login_id = models.ForeignKey(LoginTable, on_delete=models.CASCADE, null=True, blank=True)

class StaffTable(models.Model):
    Staff_code = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    Designation = models.CharField(max_length=20, null=True, blank=True)
    assigned_counter = models.IntegerField(null=True, blank=True)
    Login_id = models.ForeignKey(LoginTable, on_delete=models.CASCADE, null=True, blank=True)


class Product_Table(models.Model):
    product_name = models.CharField(max_length=20, null=True, blank=True)
    Brand = models.CharField(max_length=20, null=True, blank=True)
    Expiry_Date = models.DateField(null=True, blank=True)
    Manufacturing_Date = models.DateField(null=True, blank=True)
    Category = models.CharField(max_length=20, null=True, blank=True)
    Supplier_Name = models.CharField(max_length=20, null=True, blank=True)
    Supplier_email = models.CharField(max_length=20, null=True, blank=True)
    Supplier_Phone = models.CharField(max_length=20, null=True, blank=True)
    Barcode = models.IntegerField(null=True, blank=True)
    Purchase_Price = models.IntegerField(null=True, blank=True)
    Selling_Price = models.IntegerField(null=True, blank=True)
    Unit = models.IntegerField(null=True, blank=True)
    Description = models.CharField(max_length=20, null=True, blank=True)
    Discount = models.CharField(max_length=20, null=True, blank=True)
    Offers = models.CharField(max_length=20, null=True, blank=True)

class StockTable(models.Model):
    Product_id = models.ForeignKey(Product_Table, on_delete=models.CASCADE, null=True, blank=True)
    Quantity = models.IntegerField(null=True, blank=True)
    Last_Updated = models.DateField(auto_now_add=True)
    Status = models.CharField(max_length=20, null=True, blank=True)


class CustomerTable(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    email = models.CharField(max_length=20, null=True, blank=True)
    Address = models.CharField(max_length=20, null=True, blank=True)
    Created_At = models.DateField(auto_now_add=True)

class DiscountTable(models.Model):
    product_id = models.ForeignKey(Product_Table, on_delete=models.CASCADE, null=True, blank=True)
    discount_type = models.CharField(max_length=20, null=True, blank=True)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)


class OrderTable(models.Model):
    bill_number = models.CharField(max_length=20, null=True, blank=True)
    customer_id = models.ForeignKey(CustomerTable, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product_Table, on_delete=models.CASCADE, null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_amoount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=20, null=True, blank=True)

class OfferTable(models.Model):
    offer_name = models.CharField(max_length=20, null=True, blank=True)
    offer_description = models.CharField(max_length=100, null=True, blank=True)
    offer_type = models.CharField(max_length=20, null=True, blank=True)
    offer_start_date = models.DateField(null=True, blank=True)
    offer_end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    product = models.ForeignKey(Product_Table, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

     
class NotificationTable(models.Model):
    product_id = models.ForeignKey(Product_Table, on_delete=models.CASCADE, null=True, blank=True)
    notification_title = models.CharField(max_length=20, null=True, blank=True)
    notification_message = models.CharField(max_length=100, null=True, blank=True)
    notification_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

     
class ComplaintTable(models.Model):
    shop_id = models.ForeignKey(ShopTable, on_delete=models.CASCADE, null=True, blank=True)
    complaint_date = models.DateTimeField(auto_now_add=True)
    complaint_description = models.CharField(max_length=100, null=True, blank=True)
    reply = models.CharField(max_length=100, null=True, blank=True)


class FeedbackTable(models.Model):
    shop_id = models.ForeignKey(ShopTable, on_delete=models.CASCADE, null=True, blank=True)
    feedback_date = models.DateTimeField(auto_now_add=True)
    feedback_description = models.CharField(max_length=100, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)

class CategoryTable(models.Model):
    shop_id = models.ForeignKey(ShopTable, on_delete=models.CASCADE, null=True, blank=True)
    category_name = models.CharField(max_length=20, null=True, blank=True)
    category_description = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
from django.contrib import admin

from RetailIQApp.models import CategoryTable, ComplaintTable, CustomerTable, DiscountTable, FeedbackTable, LoginTable, NotificationTable, OfferTable, OrderTable, Product_Table, ShopTable, StaffTable, StockTable

# Register your models here.

admin.site.register(LoginTable)
admin.site.register(ShopTable)
admin.site.register(StaffTable)
admin.site.register(Product_Table)
admin.site.register(StockTable)
admin.site.register(CustomerTable)
admin.site.register(DiscountTable)
admin.site.register(OrderTable)
admin.site.register(OfferTable)
admin.site.register(NotificationTable)
admin.site.register(ComplaintTable)
admin.site.register(FeedbackTable)
admin.site.register(CategoryTable)

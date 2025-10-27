from django.contrib import admin

# Register your models here.
from .models import RiceProduct, Order, OrderItem, LaundryBooking, LogisticsOrder, LogisticsStatusUpdate

admin.site.register(RiceProduct)
admin.site.register(Order)
admin.site.register(OrderItem)

@admin.register(LaundryBooking)
class LaundryBookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'service_type', 'pickup_date', 'delivery_option', 'created_at')
    search_fields = ('full_name', 'phone', 'email')
    list_filter = ('service_type', 'delivery_option', 'pickup_date', 'created_at')
class LogisticsStatusInline(admin.TabularInline):
    model = LogisticsStatusUpdate
    extra = 0
    readonly_fields = ('status', 'note', 'timestamp')
    can_delete = False

@admin.register(LogisticsOrder)
class LogisticsOrderAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'full_name', 'status', 'vehicle_type', 'created_at')
    inlines = [LogisticsStatusInline]
    readonly_fields = ('tracking_id', 'created_at')
    search_fields = ('tracking_id', 'full_name', 'phone', 'email', 'pickup_address', 'destination')
    list_filter = ('status', 'vehicle_type', 'created_at')
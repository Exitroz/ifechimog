from django.db import models
import uuid
from django.core.mail import send_mail
# Create your models here.

class RiceProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='rice_products/')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Delivered', 'Delivered'),
    )
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_reference = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.full_name}"


class OrderItem(models.Model):
    product = models.ForeignKey(RiceProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class LaundryBooking(models.Model):
    SERVICE_CHOICES = [
        ('Wash & Fold', 'Wash & Fold'),
        ('Dry Cleaning', 'Dry Cleaning'),
        ('Ironing', 'Ironing'),
    ]

    DELIVERY_CHOICES = [
        ('Pickup & Delivery', 'Pickup & Delivery'),
        ('Pickup Only', 'Pickup Only'),
        ('Drop-off at Store', 'Drop-off at Store'),
    ]

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    quantity = models.PositiveIntegerField()
    address = models.TextField()
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    delivery_option = models.CharField(max_length=50, choices=DELIVERY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.service_type} ({self.created_at.strftime('%Y-%m-%d')})"


# class LogisticsRequest(models.Model):
#     VEHICLE_CHOICES = (
#         ('Bike', 'Bike'),
#         ('Truck', 'Truck'),
#     )
#     STATUS_CHOICES = (
#         ('Pending', 'Pending'),
#         ('In Transit', 'In Transit'),
#         ('Delivered', 'Delivered'),
#     )
#     full_name = models.CharField(max_length=150)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)
#     pickup_address = models.TextField()
#     delivery_address = models.TextField()
#     vehicle_type = models.CharField(max_length=50, choices=VEHICLE_CHOICES)
#     package_description = models.TextField()
#     tracking_id = models.CharField(max_length=50, unique=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
#     requested_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.tracking_id} - {self.full_name}"
    

class LogisticsOrder(models.Model):
    VEHICLE_CHOICES = [
        ('Bike', 'Bike'),
        ('Van', 'Van'),
        ('Truck', 'Truck'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Dispatched', 'Dispatched'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
    ]

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    pickup_address = models.TextField()
    destination = models.TextField()
    package_weight = models.DecimalField(max_digits=6, decimal_places=2)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_CHOICES)
    tracking_id = models.CharField(max_length=20, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def send_status_email(self):
        try:
            send_mail(
                subject=f"Package Update - {self.tracking_id}",
                message=(
                    f"Hello {self.full_name},\n\n"
                    f"Your package status has been updated to: {self.status}.\n\n"
                    f"Thank you for choosing Ifechimog Logistics."
                ),
                from_email='noreply@ifechimog.com',
                recipient_list=[self.email],
                fail_silently=False
            )
        except Exception as e:
            print("Email failed:", e)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        old_status = None

        if not is_new:
            old = LogisticsOrder.objects.get(id=self.id)
            old_status = old.status

        # Generate tracking ID if not already set
        if not self.tracking_id:
            self.tracking_id = f"LOG-{uuid.uuid4().hex[:8].upper()}"

        super().save(*args, **kwargs)

        # Send email only if status was changed
        if not is_new and old_status != self.status:
            self.send_status_email()

    def __str__(self):
        return f"{self.tracking_id} - {self.status}"
    
class LogisticsStatusUpdate(models.Model):
    order = models.ForeignKey(LogisticsOrder, on_delete=models.CASCADE, related_name='status_updates')
    status = models.CharField(max_length=20)
    note = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.status} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
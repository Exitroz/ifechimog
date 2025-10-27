from django.shortcuts import render, redirect, get_object_or_404
from .models import RiceProduct, Order, OrderItem, LogisticsOrder
from .forms import LaundryBookingForm, CheckoutForm, LogisticsOrderForm
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
import requests
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def rice(request):
    products = RiceProduct.objects.filter(is_available=True)
    return render(request, 'rice.html', {'products': products})


# --- CART PAGE ---
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = RiceProduct.objects.get(id=product_id)
        item_total = product.price * quantity
        total += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def add_to_cart(request, product_id):
    product = get_object_or_404(RiceProduct, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('cart')


# --- REMOVE FROM CART ---
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('cart')


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            total = 0
            for product_id, quantity in cart.items():
                product = RiceProduct.objects.get(id=product_id)
                total += product.price * quantity
            order.total_amount = total
            order.status = 'Pending'
            order.save()

            for product_id, quantity in cart.items():
                product = RiceProduct.objects.get(id=product_id)
                OrderItem.objects.create(order=order, product=product, quantity=quantity)

            request.session['cart'] = {}
            return redirect('pay_order', order_id=order.id)
    else:
        form = CheckoutForm()

    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = RiceProduct.objects.get(id=product_id)
        item_total = product.price * quantity
        total += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    return render(request, 'checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total,
    })

def pay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'pay_order.html', {
        'order': order,
        'PAYSTACK_PUBLIC_KEY': settings.PAYSTACK_PUBLIC_KEY
    })

def verify_payment(request, order_id, ref):
    order = get_object_or_404(Order, id=order_id)

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }
    url = f"https://api.paystack.co/transaction/verify/{ref}"
    response = requests.get(url, headers=headers)
    data = response.json()

    if data.get('status') and data['data']['status'] == 'success':
        order.status = 'Paid'
        order.payment_reference = ref
        order.save()

        # send_mail(
        #     subject="Order Payment Confirmed",
        #     message=f"Dear {order.full_name}, your payment was successful!",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[order.email]
        # )
        email = EmailMessage(
            subject="Order Payment Confirmed",
            body=f"Dear {order.full_name}, your payment was successful!",
            to=[order.email],  
        )
        email.send()
        return redirect('order_success')
    else:
        return HttpResponse("Payment verification failed.")


@csrf_exempt
def paystack_webhook(request):
    if request.method == 'POST':
        payload = request.body
        event = None

        try:
            event = json.loads(payload)
        except ValueError:
            return HttpResponse(status=400)

        # Verify it's a payment success event
        if event['event'] == 'charge.success':
            data = event['data']
            reference = data['reference']

            # Find and update order
            try:
                order = Order.objects.get(payment_reference=reference)
                order.status = 'Paid'
                order.save()
            except Order.DoesNotExist:
                pass  # Optionally log

        return HttpResponse(status=200)

    return HttpResponse(status=405)

def order_success(request):
    return render(request, 'order-success.html')

def track_order(request):
    return render(request, 'track-order.html')

def laundry_booking(request):
    if request.method == 'POST':
        form = LaundryBookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # send confirmation email
            try:
                # send_mail(
                #     subject="Laundry Booking Confirmed",
                #     message=f"Hi {booking.full_name},\n\nYour laundry booking for {booking.service_type} has been received.\n\nPickup Date: {booking.pickup_date}, Time: {booking.pickup_time}\nDelivery Option: {booking.delivery_option}\n\nThank you!",
                #     from_email="noreply@ifechimog.com",
                #     recipient_list=[booking.email],
                #     fail_silently=False
                # )
                # Send email
                email = EmailMessage(
                    subject="Laundry Booking Confirmed",
                    body=f"Hi {booking.full_name},\n\nYour laundry booking for {booking.service_type} has been received.\n\nPickup Date: {booking.pickup_date}, Time: {booking.pickup_time}\nDelivery Option: {booking.delivery_option}\n\nThank you!",
                    to=[booking.email],  
                )
                email.send()

            except Exception as e:
                print("Email failed:", e)

            return render(request, 'booking_success.html', {'booking': booking})
    else:
        form = LaundryBookingForm()
    return render(request, 'laundry.html', {'form': form})

def laundry_price(request):
    return render(request, 'laundry-price.html')

def booking_success(request):
    return render(request, 'booking-success.html')


def logistics_request(request):
    form = LogisticsOrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        order = form.save()
        return render(request, 'logistics_success.html', {'order': order})
    return render(request, 'logistics_form.html', {'form': form})

def track_order(request):
    tracking_id = request.GET.get('tracking_id')
    order = None
    if tracking_id:
        try:
            order = LogisticsOrder.objects.get(tracking_id=tracking_id)
        except LogisticsOrder.DoesNotExist:
            order = None
    return render(request, 'track_order.html', {'order': order})

def contact(request):
    return render(request, 'contact.html')

def support(request):
    return render(request, 'support.html')

def support_widget(request):
    return render(request, 'support-widget.html')
"""
URL configuration for ifechimog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from ifechimog_app import views
from ifechimog_app.views import paystack_webhook
from django.contrib.sitemaps.views import sitemap
from ifechimog_app.sitemaps import StaticViewSitemap
from django.conf import settings
from django.conf.urls.static import static


sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('rice/', views.rice, name='rice'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('track-order/', views.track_order, name='track_order'),
    path('laundry/', views.laundry_booking, name='laundry_booking'),
    path('laundry-price/', views.laundry_price, name='laundry_price'),
    path('booking-success/', views.booking_success, name='booking_success'),
    # path('logistics/', views.logistics, name='logistics'),
    path('contact/', views.contact, name='contact'),
    path('support/', views.support, name='support'),
    path('support-widget/', views.support_widget, name='support_widget'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('paystack/webhook/', paystack_webhook, name='paystack_webhook'),
    path('pay/<int:order_id>/', views.pay_order, name='pay_order'),
    path('verify-payment/<int:order_id>/<str:ref>/', views.verify_payment, name='verify_payment'),
    path('logistics/', views.logistics_request, name='logistics_request'),
    path('track-order/', views.track_order, name='track_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
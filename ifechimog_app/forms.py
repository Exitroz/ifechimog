from django import forms
from .models import LaundryBooking, Order, LogisticsOrder

class LogisticsOrderForm(forms.ModelForm):
    class Meta:
        model = LogisticsOrder
        fields = ['full_name', 'email', 'phone', 'pickup_address', 'destination', 'package_weight', 'vehicle_type']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'pickup_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'destination': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'package_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
        }

class LaundryBookingForm(forms.ModelForm):
    class Meta:
        model = LaundryBooking
        fields = [
            'full_name', 'phone', 'email', 'service_type', 'quantity',
            'address', 'pickup_date', 'pickup_time', 'delivery_option'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pickup_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'delivery_option': forms.Select(attrs={'class': 'form-select'}),
        }
# class LogisticsRequestForm(forms.ModelForm):
#     class Meta:
#         model = LogisticsRequest
#         fields = ['full_name', 'email', 'phone', 'pickup_address', 'delivery_address',
#                   'vehicle_type', 'package_description']

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address']
        email = forms.EmailField(widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class': 'form-control',
        }))

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
                'id': 'id_full_name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'id': 'id_email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'id': 'id_phone'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street Address',
                'id': 'id_address'
            }),
            # 'city': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'City',
            #     'id': 'id_city'
            # }),
            # 'state': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'State',
            #     'id': 'id_state'
            # }),
        }
from django import forms

class OrderForm(forms.Form):
    order_count = forms.IntegerField(initial=0)
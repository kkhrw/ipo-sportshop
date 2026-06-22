from django import forms


class CheckoutForm(forms.Form):
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Введите полный адрес доставки: город, улица, дом, квартира, индекс',
            'style': 'width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 10px; font-size: 16px; resize: vertical;'
        }),
        label="📍 Адрес доставки",
        help_text="Укажите полный адрес, включая город, улицу, дом и квартиру"
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@mail.com',
            'style': 'width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 10px; font-size: 16px;'
        }),
        label="📧 Email для получения чека",
        help_text="На этот адрес будет отправлен чек в формате Excel"
    )
    
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': '+375 (XX) XXX-XX-XX',
            'style': 'width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 10px; font-size: 16px;'
        }),
        label="📱 Контактный телефон",
        required=False,
        help_text="Необязательно, но желательно для связи"
    )
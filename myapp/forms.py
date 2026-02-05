from django import forms
from django.contrib.auth.models import User

from .models import Product, Order, CustomUser


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'in_stock', 'category']



 # Регистрация с двумя паролями, мейлом, телефоном и тд
class RegisterForm(forms.ModelForm):

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password']

        labels = {'username': 'Имя пользователя',
                  'phone': 'Номер телефона',
                  'email': 'Ваша почта',
                  'first_name': 'Имя',
                  'last_name': 'Фамилия',
                  }

    #тут маленькие плюшки для фронта
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-input'})
        self.fields['username'].help_text = None

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data


#форма для заказа и последующего отправления в тг бота
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'telephone', 'email']

        labels = {
            'name': 'Ваше имя',
            'telephone': 'Номер телефона',
            'email': 'Электронная почта'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-input'})


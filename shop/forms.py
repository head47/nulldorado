from django import forms
from django.utils.translation import gettext_lazy as _

class SearchForm(forms.Form):
    query = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control'}), max_length=64)

class OrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        try:
            itemid = kwargs.pop('itemid')
        except KeyError:
            itemid = 0
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['id'] = forms.IntegerField(label='', widget=forms.HiddenInput(), initial=itemid)
        self.fields['amount'] = forms.IntegerField(label='Добавление в корзину', widget=forms.NumberInput(attrs={'type':'range','class':'custom-range','min':0,'max':10,'id':'Range_'+str(itemid)}), initial=1)

class SubmitOrderForm(forms.Form):
    number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', required=True,label='Номер телефона',max_length=16,
        error_messages={'invalid': _("Формат номера телефона не верен."),'required': _("Номер телефона обязателен.")})
    email = forms.EmailField(max_length=64,required=True,label='e-mail')

from django import forms

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
        self.fields['amount'] = forms.IntegerField(label='Добавление в корзину', widget=forms.NumberInput(attrs={'type':'range','class':'custom-range','min':1,'max':10,'id':'Range_'+str(itemid)}), initial=1)

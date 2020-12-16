from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control'}), max_length=64)

class OrderForm(forms.Form):
    def __init__(self, itemid):
        super().__init__()
        self.fields['id'] = forms.IntegerField(label='', widget=forms.HiddenInput(), initial=itemid)
        self.fields['amount'] = forms.IntegerField(label='Добавление в корзину', widget=forms.NumberInput(attrs={'type':'range','class':'custom-range','min':0,'max':10,'id':'Range_'+str(itemid)}))

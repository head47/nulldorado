from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control'}), max_length=64)

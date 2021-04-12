from django import forms


class TextForm(forms.Form):
    legal_shit = forms.CharField(widget=forms.Textarea)
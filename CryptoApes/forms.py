from django import forms
from CryptoApes.models import stakedToken

class LogStakedToken(forms.ModelForm):
    class Meta:
        model = stakedToken
        fields = ("message",)   # NOTE: the trailing comma is required
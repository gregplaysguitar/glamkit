from django import forms
from django.forms.widgets import HiddenInput


class TellAFriendForm(forms.Form):
    url = forms.CharField(widget=HiddenInput(), max_length=255)
    sender_name = forms.CharField(label='Your Name', max_length=80)
    sender_email = forms.EmailField(label='Your Email')
    recipient_email = forms.EmailField(label='Friend\'s Email')
#    recipient_name = forms.CharField(label='Your Friend\'s Name', max_length=80)
    personal_message = forms.CharField(label="Message", required=False, max_length=255, widget=forms.Textarea(attrs={'cols':45, 'rows':9}), help_text='255 characters maximum')

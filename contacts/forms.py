__author__ = 'basa'
# encoding: utf-8

from django import forms
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Contact, Address


ContactAddressFormSet = inlineformset_factory(Contact, Address)


class ContactForm(forms.ModelForm):
    confirm_email = forms.EmailField(label=u'Подтверждение email', required=True)

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            email = kwargs['instance'].email
            kwargs.setdefault('initial', {})['confirm_email'] = email
        return super(ContactForm, self).__init__(*args, **kwargs)

    def clean(self):
        if (self.cleaned_data.get('email') !=
                self.cleaned_data.get('confirm_email')):
            raise ValidationError('Email должны совпадать')
        return self.cleaned_data

    class Meta:
      model = Contact

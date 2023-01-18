from django.forms import forms
from django import forms
from django.forms import ModelForm, modelform_factory
from . import models


class listing_form(ModelForm):
    class Meta:
        model = models.listing
        fields = ['bid_price', 'title', 'description', 'category', 'image',]
        

comment_form = modelform_factory(models.comments, fields=('comment',))

bids_form =  modelform_factory(models.bids, fields=('value',))

class close_listing_form(forms.Form):
        status = forms.CharField()



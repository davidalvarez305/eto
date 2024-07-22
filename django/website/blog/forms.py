from django import forms

class QuoteForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15)
    service = forms.IntegerField()
    location = forms.IntegerField()
    message = forms.CharField(widget=forms.Textarea)
    bathrooms = forms.IntegerField()
    total_rooms = forms.IntegerField()
    square_feet = forms.FloatField()
    pets = forms.IntegerField()
    is_house = forms.BooleanField()
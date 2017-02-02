from django import forms

class communityForm(forms.Form):
      community = forms.CharField(label='Community Name',max_length=100)
      percentage = forms.FloatField (label='percentage',min_value=0.0, max_value=1.0)


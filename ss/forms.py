from django import forms
from ss.models import Sample, lookup_table,PCR_target
from dal import autocomplete


class SearchForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class fileUpload(forms.Form):
    file = forms.FileField()


class SampleSelection(forms.Form):
    sample = forms.ModelChoiceField(queryset=Sample.objects.all())


class lookupForm(forms.ModelForm):
    class Meta:
        model = lookup_table
        fields = ('__all__')
        widgets = {
            'species': autocomplete.ModelSelect2(url='lookup-autocomplete')
        }

class Correlated_Filter(forms.Form):
    target = forms.ModelChoiceField(queryset=PCR_target.objects.all())
    reads = forms.IntegerField()

class Correlated_landscape_form(forms.Form):
    target = forms.ModelChoiceField(queryset=PCR_target.objects.all())
    max = forms.IntegerField()
    step = forms.IntegerField()

class CorrelatedPlotForm(forms.Form):
    target = forms.ModelChoiceField(queryset=PCR_target.objects.all())
from django import forms
from tagging.models import Tag


class SearchForm(forms.Form):
    search_term = forms.CharField(required=True)
    tag = forms.ModelMultipleChoiceField(required=False,queryset=Tag.objects.all())
    
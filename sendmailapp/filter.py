from django_filters import FilterSet
from .models import Patient,Group
import django_filters
from django import forms

class PatientFilter(FilterSet):
    groups = django_filters.ModelChoiceFilter(queryset=Group.objects.all(),widget=forms.Select)

    class Meta:
        model = Patient
        fields =['groups',]

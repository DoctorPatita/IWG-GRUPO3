from django import forms

from organization.models import Organization

class CreateOrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'description']
from import_export import resources, fields, widgets
from .models import PatientGroup,Patient


class PatientResource(resources.ModelResource):
    class Meta:
        model = Patient
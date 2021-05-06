from django import forms
from .models import Patient,Group
from tinymce.widgets import TinyMCE
from django_select2 import forms as s2forms
from bootstrap_datepicker_plus import DatePickerInput
from bootstrap_modal_forms.forms import BSModalModelForm

#from .tasks import send_review_email_task



class GroupModelForm(BSModalModelForm):
    class Meta:
        model = Group
        fields =('name',)




class GroupWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        'name__icontains',
    ]
    queryset = Group.objects.all()


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields =('name','gender','dob','email','groups')
       # groups =forms.ModelMultipleChoiceField(queryset=Group.objects.all())
        widgets ={
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'gender': forms.Select(attrs={'class':'form-control'}),
            'dob':DatePickerInput(),
            #'dob': forms.TextInput(attrs={'id':'dp1','class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'groups':GroupWidget(attrs={'class':'form-control'}),
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
        widgets ={
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }





class SendMail(forms.Form):
#    To = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    Subject = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    Message = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 15}))

    class Media:
        js = ('/site_media/static/tiny_mce/tinymce.min.js',)






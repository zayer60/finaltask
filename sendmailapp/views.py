import csv
import io
import openpyxl
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, FormView
from .models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .form import PatientForm, SendMail, GroupForm, GroupModelForm
from django.http import HttpResponse, HttpResponseRedirect
from tablib import Dataset
from .resources import PatientResource
from .tasks import send_review_email_task
from django.core.mail import send_mail, BadHeaderError
from .filter import PatientFilter
from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)
from io import TextIOWrapper




class GroupCreateView(BSModalCreateView):
    template_name = 'sendmailapp/create_group.html'
    form_class = GroupModelForm
    success_url = reverse_lazy('')


class GroupUpdateView(BSModalUpdateView):
    model = Group
    template_name = 'sendmailapp/update_modal.html'
    form_class = GroupModelForm
    success_url = reverse_lazy('')


class GroupDeleteView(BSModalDeleteView):
    model = Group
    template_name = 'sendmailapp/delete_group.html'
    success_url = reverse_lazy('')










class GroupListView(ListView):
    model = Group
    template_name = 'sendmailapp/grouplist.html'

def groupdetail(request,id):
    group= Group.objects.get(pk=id)
    patients=group.patient_set.all()
    return render(request,'sendmailapp/groupdetail.html',{'group':group,'patients':patients})

class CreateGroup( CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'sendmailapp/create_modal.html'
    success_url = reverse_lazy('group-list')

class UpdateGroup( UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'sendmailapp/update_modal.html'
    success_url = reverse_lazy('group-list')

class DeleteGroup( DeleteView):
    model = Group
    template_name = 'sendmailapp/delete_modal.html'
    success_url = reverse_lazy('group-list')

class PatientListView(ListView):
    model = Patient
    template_name = 'sendmailapp/patientlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PatientFilter(self.request.GET,queryset=self.get_queryset())
        return context


class CreatePatient( CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'sendmailapp/patient-create.html'

class UpdatePatient( UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'sendmailapp/patient-update-form.html'


class DeletePatient( DeleteView):
    model = Patient
    template_name = 'sendmailapp/delete_patient_modal.html'
    success_url = reverse_lazy('patient-list')

class SearchPatient(ListView):
    model = Patient
    context_object_name = 'patient_list'
    template_name = 'sendmailapp/search-patient.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Patient.objects.filter(name__icontains=query)





def export(request):
    patient_resource = PatientResource()
    dataset = patient_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response


def simple_upload(request):
    if request.method == 'POST':
        patient_resource = PatientResource()
        dataset = Dataset()
        new_patients = request.FILES['myfile']
        #import_data = dataset.load(new_patients.read(), format='xlsx')
        imported_data = dataset.load(new_patients.read(), format='xlsx')
        for data in imported_data:
            pat,created = Patient.objects.get_or_create(pk=data[0])
            pat.groups.all().delete()
            pat.save()
            #print(patient)
            grouplist = data[5].split(':')
            for group in grouplist:

                group,created= Group.objects.get_or_create(name=group)
                print(group)

                value= PatientGroup(patient=pat,group=group)
                print(value)
                value.save()

            '''
            value = PatientGroup(
                data[0],
                data[1],
                data[2],
            )
            '''


            # result = patient_resource.import_data(dataset, dry_run=True)  # Test the data import

        # if not result.has_errors():
        #    person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'sendmailapp/index.html')





'''
class ContactView(FormView):
    template_name = 'sendmailapp/form.html'
    form_class = SendMail
'''


def sendemail(request,id):
    form = SendMail()
    if request.method== 'POST':
        form = SendMail(request.POST)
        if form.is_valid():
            patient = Patient.objects.get(pk=id)
            to = [patient.email]
            print(to)
            try:
                send_review_email_task.delay(
                    form.cleaned_data['Subject'],'hello there',form.cleaned_data['Message'] , to)
                return HttpResponseRedirect(reverse('group-list'))
                #return HttpResponse('success')
            except BadHeaderError:
                return HttpResponse('invalid header found')
    return render(request, 'sendmailapp/form.html', {'form': form})



def groupemail(request,id):
    group = Group.objects.get(pk=id)
    patients = group.patient_set.all()
    to = [patient.email for patient in patients]
    print(to)
    form = SendMail()
    if request.method=='POST':
        form = SendMail(request.POST)
        if form.is_valid():
                print(to)
                send_review_email_task.delay(
                    form.cleaned_data['Subject'],'hello there', form.cleaned_data['Message'], to)
                return HttpResponseRedirect(reverse('group-list'))
                #return HttpResponse('success')
    return render(request, 'sendmailapp/form.html', {'form': form})

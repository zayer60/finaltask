from django.urls import path
from .views import *

urlpatterns = [
    path('',GroupListView.as_view(),name='group-list'),
    path('<int:id>/',groupdetail,name='group-details'),
    path('<int:pk>/edit/',UpdateGroup.as_view(),name='group-update'),
    path('create/',CreateGroup.as_view(),name='group-create'),
    path('<int:pk>/delete/',DeleteGroup.as_view(),name='group-delete'),
    path('patient/', PatientListView.as_view(), name='patient-list'),
    path('patient/create/', CreatePatient.as_view(), name='create-patient'),
    path('patient/<int:pk>/edit/', UpdatePatient.as_view(), name='update-patient'),
    path('patient/<int:pk>/delete', DeletePatient.as_view(), name='delete-patient'),
    path('search/', SearchPatient.as_view(), name='search_results'),
    path('export/', export,name='export'),
    path('upload/', simple_upload,name='uplaod'),
    #path('send/',ContactView.as_view(), name='send-email'),
    path('send/<int:id>/',sendemail,name='sendemail'),
    path('sendgroup/<int:id>',groupemail,name= 'sendgroupemail'),
    #path('uploadcsv/',simplyupload,name ='uploadexcel'),

]
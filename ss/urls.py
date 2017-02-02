from django.conf.urls import url,include
from . import views

urlpatterns = [
    url (r'^$', views.index, name='sq_index'),
	url (r'^karen/$', views.SS_upload, name='karen_upload'),
	url (r'^pcr/$', views.PCR_upload, name='pcr_upload'),
    url (r'^reads/$',views.Reads_upload,name='reads_upload'),
	url ('lookup-autocomplete/$',views.lookupAutocomplete.as_view(),name='lookup-autocomplete',),
    url (r'^correlated/$',views.correlated_table,name='correlated_result',),
    url (r'^correlated/reads/$',views.correlated_table_filter,name='correlated_result',),
    url (r'^correlated/landscape/$',views.correlated_table_ls_view,name='correlated_landscape',),
    url (r'^correlated/plot/$',views.correlated_plot,name='correlated_plot',),
    url (r'^correlated/(?P<sampleID>[0-9]+)/$',views.sample_details,name='sample_details',)
]
from django.conf.urls import url,include
from . import views

urlpatterns = [
    url (r'^$', views.index, name='sq_index'),
	url (r'^nt/$', views.nt, name='sq_nt'),
	url (r'^aa/$', views.aa, name='sq_aa'),
	url (r'^aa/final/$', views.aa_final, name='sq_aa_final'),
	url (r'^aa/complete/$', views.aa_com, name='sq_aa_final'),
	url (r'^aa/partial/$', views.aa_part, name='sq_aa_final'),
]
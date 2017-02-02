from django.conf.urls import url,include
from . import views

urlpatterns = [
    url (r'^$', views.index, name='mix_index'),
    url (r'^download/$', views.file_streaming, name='mix_index'),
    url (r'^hw/$', views.highlight_word, name='high_light'),

]

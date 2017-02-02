from django.contrib import admin

# Register your models here.


# Register your models here.
from .models import *

admin.site.register(Species)
admin.site.register(Sample)
admin.site.register(ss_data)
admin.site.register(PCR_detail)
admin.site.register(PCR_data)
admin.site.register(PCR_target)


from .forms import lookupForm
class lookupAdmin(admin.ModelAdmin):
    form = lookupForm

admin.site.register(lookup_table,lookupAdmin)
admin.site.register(Sample_reads)
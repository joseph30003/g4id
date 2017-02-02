from django.shortcuts import render

# Create your views here.
from ss.models import Species, Sample, ss_data, PCR_detail,lookup_table,PCR_target,PCR_data,Sample_reads
from ss.forms import fileUpload, SampleSelection,Correlated_Filter,Correlated_landscape_form,CorrelatedPlotForm


def block_parser(block):
    line_1 = block[0].split('\t')
    s_type = line_1[0]
    samples = {}
    species = []
    index = 0
    for i in line_1[1:]:
        samples[index] = i.split('_')[0]

        index = index + 1
    for line in block[1:]:
        l = line.split('\t')
        s = {}
        s['name'] = l[0]
        s_data = {}
        index = 0
        for d in l[1:]:
            s_data[samples[index]] = d
            index = index + 1
        s['data'] = s_data
        species.append(s)

    return {'type': s_type, 'species': species}


def insert_sampleID(sample):
    try:
        Sample.objects.get(name=sample)
    except:
        s = Sample()
        s.name = sample
        s.save()

    return Sample.objects.get(name=sample)

def insert_Target(target):
    try:
        PCR_target.objects.get(name=target)
    except:
        t = PCR_target()
        t.name = target
        t.save()
    return PCR_target.objects.get(name=target)


def insert_speies(name, type):
    try:
        Species.objects.get(name=name, type=type)
    except:
        s = Species()
        s.name = name
        s.type = type
        s.save()
    return Species.objects.get(name=name, type=type)


def karen_file_handler(f):
    block = []
    blocks = []
    lines = []
    for chunk in f.chunks():
        for l in chunk.decode('utf-8').splitlines():
            lines.append(l)

    for line in lines:
        if "#" in line:
            blocks.append(block)
            block = []

        else:
            block.append(line)
    blocks.append(block)

    for b in blocks:
        block_dic = block_parser(b)

        stype = block_dic['type']
        for s in block_dic['species']:

            species = insert_speies(s['name'], stype)
            data = s['data']
            for key, value in data.items():
                sample = insert_sampleID(key)
                ss = ss_data()
                ss.sample = sample
                ss.species = species
                ss.count = value
                ss.save()


def SS_upload(request):
    if request.method == 'POST':
        form = fileUpload(request.POST, request.FILES)
        if form.is_valid():
            karen_file_handler(request.FILES['file'])

    else:
        form = fileUpload()

    return render(request, 'upload.html', {'form': form})


import math


def nodelist(objs, type):
    rs = []
    ex_d = 0
    for b in objs:
        node = {}

        if b.count:
            node['name'] = b.species.name
            node['count'] = b.count
            node['type'] = type
            node['r'] = int(math.log10(b.count) + 1) * 10

            node['cy'] = node['r'] + 15 + ex_d
            ex_d = node['cy'] + node['r']
            rs.append(node)

    return rs


import json


def index(request):
    virus = []
    bacteria = []
    fungi = []

    if request.method == 'POST':
        form = SampleSelection(request.POST)
        sample = Sample.objects.get(id=form.data['sample'])
        d = ss_data.objects.filter(sample=sample)

        virus = nodelist(d.filter(species__type='Virus').order_by('-count'), 'virus')

        bacteria = nodelist(d.filter(species__type='Bacteria').order_by('-count'), 'bacteria')

        fungi = nodelist(d.filter(species__type='Fungi').order_by('-count'), 'fungi')
        # data.extend (nodelist (fungi, 'fungi'))

    else:
        form = SampleSelection()

    return render(request, 'ss_index.html', {'form': form, 'virus': virus, 'fungi': fungi, 'bacteria': bacteria})

def sample_details(request,sampleID=1):
    sample = Sample.objects.get(id=sampleID)
    pcr_rs = []
    try:
        pcr = PCR_data.objects.filter(sample=sample)

        for p in pcr:
            pcr_rs.append(p.target.name)
    except:
        pcr_rs = []

    d = ss_data.objects.filter(sample=sample)

    virus = nodelist(d.filter(species__type='Virus').order_by('-count'), 'virus')

    bacteria = nodelist(d.filter(species__type='Bacteria').order_by('-count'), 'bacteria')

    fungi = nodelist(d.filter(species__type='Fungi').order_by('-count'), 'fungi')


    return render(request, 'ss_details.html', {'PCR':pcr_rs, 'virus': virus, 'fungi': fungi, 'bacteria': bacteria})


def PCR_file_handler(f):
    lines = []
    for chunk in f.chunks():
        for l in chunk.decode('utf-8').splitlines():
            lines.append(l)

    for line in lines:
        elements = line.split(',')
        pcr = PCR_detail()
        pcr.sample = insert_sampleID(elements[0])
        pcr.ward_1 = elements[1]
        pcr.ward_2 = elements[2]
        pcr.age = elements[3]
        pcr.PCR = elements[4]
        pcr.PCR_result = elements[5]
        if elements[6]:
            pcr.RPPCR_date = elements[6]
        else:
            pcr.RPPCR_date = 0
        pcr.save()
        positives = elements[7:10]
        for p in positives:
            if p and p.lower() !='neg' :
                target = insert_Target(str(p))
                pcr_data = PCR_data()
                pcr_data.sample = pcr.sample
                pcr_data.target = target
                pcr_data.save()




def PCR_upload(request):
    if request.method == 'POST':
        form = fileUpload(request.POST, request.FILES)
        if form.is_valid():
            PCR_file_handler(request.FILES['file'])

    else:
        form = fileUpload()

    return render(request, 'upload.html', {'form': form})

def Reads_file_handler(f):
    lines = []
    for chunk in f.chunks():
        for l in chunk.decode('utf-8').splitlines():
            lines.append(l)

    for line in lines:
        elements = line.split(',')
        sr = Sample_reads()
        sr.sample = insert_sampleID(elements[0].split('_')[0])
        sr.reads = elements[1]
        sr.save()

def Reads_upload(request):
    if request.method == 'POST':
        form = fileUpload(request.POST, request.FILES)
        if form.is_valid():
            Reads_file_handler(request.FILES['file'])

    else:
        form = fileUpload()

    return render(request, 'upload.html', {'form': form})

from dal import autocomplete

class lookupAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Species.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


def correlated_rs(targetID):
    target = PCR_target.objects.get(id=targetID)
    samples = Species.objects.prefetch_related('ss_data_set', 'lookup_table_set').filter(lookup_table__positive=target,
                                                                                         ss_data__count__gt=0).values(
        'ss_data__sample').distinct()
    karen_positive = set(s['ss_data__sample'] for s in samples)

    pcr_positive = set(pcr.sample.id for pcr in PCR_data.objects.filter(target=target))
    pcr_negtive = set(pcr.sample.id for pcr in PCR_detail.objects.all()) - pcr_positive
    f_negative = pcr_positive - karen_positive
    t_positive = pcr_positive - f_negative
    t_negative = pcr_negtive - karen_positive
    f_positive = pcr_negtive - t_negative
    correlated_rs = []
    for s in t_positive:
        rs = {}
        rs['s_id'] = s
        rs['s_name'] = Sample.objects.get(id=s)
        rs['PCR'] = True
        rs['karen'] = True
        rs['cr'] = "True Positive"
        correlated_rs.append(rs)
    for s in f_positive:
        rs = {}
        rs['s_id'] = s
        rs['s_name'] = Sample.objects.get(id=s)
        rs['PCR'] = False
        rs['karen'] = True
        rs['cr'] = "False Positive"
        correlated_rs.append(rs)
    for s in t_negative:
        rs = {}
        rs['s_id'] = s
        rs['s_name'] = Sample.objects.get(id=s)
        rs['PCR'] = False
        rs['karen'] = False
        rs['cr'] = "True Negative"
        correlated_rs.append(rs)
    for s in f_negative:
        rs = {}
        rs['s_id'] = s
        rs['s_name'] = Sample.objects.get(id=s)
        rs['PCR'] = True
        rs['karen'] = False
        rs['cr'] = "False Negative"
        correlated_rs.append(rs)
    landscape = {'tp': t_positive.__len__(), 'fp': f_positive.__len__(), 'tn': t_negative.__len__(),
                 'fn': f_negative.__len__()}

    return {'target':target.name,'statics':landscape,'rs_list':correlated_rs}


def correlated_with_reads(targetID,reads):
    target = PCR_target.objects.get(id=targetID)
    ex_samples = set(sr.sample.id for sr in Sample_reads.objects.filter(reads__lt=reads))

    samples = Species.objects.prefetch_related('ss_data_set', 'lookup_table_set').filter(lookup_table__positive=target,
                                                                                         ss_data__count__gt=0).values(
        'ss_data__sample').distinct()
    s_with_reads = set(s.sample.id for s in Sample_reads.objects.all())
    s_without_reads = set(s.id for s in Sample.objects.all()) - s_with_reads

    karen_positive = set(s['ss_data__sample'] for s in samples)

    ex_samples = ex_samples | s_without_reads


    pcr_positive = set(pcr.sample.id for pcr in PCR_data.objects.filter(target=target))
    pcr_negtive = (set(pcr.sample.id for pcr in PCR_detail.objects.all()))- pcr_positive
    f_negative = pcr_positive - karen_positive - ex_samples

    t_positive = pcr_positive - f_negative - ex_samples
    t_negative = pcr_negtive - karen_positive - ex_samples
    f_positive = pcr_negtive - t_negative - ex_samples
    correlated_rs = []

    for s in t_positive:
        rs = {}
        rs['s_id'] = s
        rs['s_name'] = Sample.objects.get(id=s)
        rs['PCR'] = True
        rs['karen'] = True
        rs['cr'] = "True Positive"
        try:
            rs['reads'] = Sample.objects.get(id=s).sample_reads_set.get().reads
        except:
            rs['reads'] = 0
        correlated_rs.append(rs)
    for s in f_positive:
        rs = {}
        rs['s_id'] = s
        rs['s_name'] = Sample.objects.get(id=s)
        rs['PCR'] = False
        rs['karen'] = True
        rs['cr'] = "False Positive"
        try:
            rs['reads'] = Sample.objects.get(id=s).sample_reads_set.get().reads
        except:
            rs['reads'] = 0
        correlated_rs.append(rs)
    for s in t_negative:
        rs = {}
        rs['s_id'] = s
        rs['s_name'] = Sample.objects.get(id=s)
        rs['PCR'] = False
        rs['karen'] = False
        rs['cr'] = "True Negative"
        try:
            rs['reads'] = Sample.objects.get(id=s).sample_reads_set.get().reads
        except:
            rs['reads'] = 0
        correlated_rs.append(rs)
    for s in f_negative:
        rs = {}
        rs['s_id'] = s
        rs['s_name'] = Sample.objects.get(id=s)
        rs['PCR'] = True
        rs['karen'] = False
        rs['cr'] = "False Negative"
        try:
            rs['reads'] = Sample.objects.get(id=s).sample_reads_set.get().reads
        except:
            rs['reads'] = 0
        correlated_rs.append(rs)
    landscape = {'tp': t_positive.__len__(), 'fp': f_positive.__len__(), 'tn': t_negative.__len__(),
                 'fn': f_negative.__len__()}

    return {'target':target.name,'statics':landscape,'rs_list':correlated_rs}

def correlated_rs_with_reads(targetID,reads):
    target = PCR_target.objects.get(id=targetID)
    ex_samples = set(sr.sample.id for sr in Sample_reads.objects.filter(reads__lt=reads))

    samples = Species.objects.prefetch_related('ss_data_set', 'lookup_table_set').filter(lookup_table__positive=target,
                                                                                         ss_data__count__gt=0).values(
        'ss_data__sample').distinct()
    s_with_reads = set(s.sample.id for s in Sample_reads.objects.all())
    s_without_reads = set(s.id for s in Sample.objects.all()) - s_with_reads

    karen_positive = set(s['ss_data__sample'] for s in samples)

    ex_samples = ex_samples | s_without_reads


    pcr_positive = set(pcr.sample.id for pcr in PCR_data.objects.filter(target=target))
    pcr_negtive = (set(pcr.sample.id for pcr in PCR_detail.objects.all()))- pcr_positive
    f_negative = pcr_positive - karen_positive - ex_samples

    t_positive = pcr_positive - f_negative - ex_samples
    t_negative = pcr_negtive - karen_positive - ex_samples
    f_positive = pcr_negtive - t_negative - ex_samples
    fn = []
    tp = []
    tn = []
    fp = []
    for s in t_positive:
        tp.append(Sample.objects.get(id=s).sample_reads_set.get().reads)
    for s in f_positive:
        fp.append(Sample.objects.get(id=s).sample_reads_set.get().reads)
    for s in t_negative:
        tn.append(Sample.objects.get(id=s).sample_reads_set.get().reads)
    for s in f_negative:
        fn.append(Sample.objects.get(id=s).sample_reads_set.get().reads)


    return fn,fp,tn,tp


def correlated_table_landscape(targetID,max,step):
    x=['x']
    fn=['fn']
    fp=['fp']
    for i in range(0,max,step):
        r = correlated_with_reads(targetID,i)
        rs = r['statics']
        x.append(i)

        fp.append(rs['fp']/(rs['fp']+rs['tp']))
        fn.append(rs['fn']/(rs['fn']+rs['tn']))

    return [x,fn,fp]

def correlated_table(request):
    targets = [p['positive'] for p in lookup_table.objects.all().values('positive').distinct()]
    rs = [correlated_rs(t) for t in targets]

    return render(request,'correlated.html',{'objs':rs})

def correlated_table_filter(request):
    if request.method == 'POST':
        form = Correlated_Filter(request.POST)
        rs = correlated_with_reads(request.POST['target'],int(request.POST['reads']))
    else:
        form = Correlated_Filter()
        rs = ''
    return render(request, 'correlated_filter.html', {'form':form,'obj': rs})
import json
def correlated_table_ls_view(request):
    if request.method == "POST":
        form = Correlated_landscape_form(request.POST)
        rs = correlated_table_landscape(request.POST['target'],int(request.POST['max']),int(request.POST['step']))
    else:
        form = Correlated_landscape_form()
        rs = []
    return render(request,"correlated_landscape.html",{'form':form,'rs':json.dumps(rs)})

def correlated_plot(request):
    fn = []
    tp = []
    tn = []
    fp = []
    if request.method == 'POST':
        form = Correlated_Filter(request.POST)
        fn, fp, tn, tp = correlated_rs_with_reads(request.POST['target'], int(request.POST['reads']))

    else:
        form = Correlated_Filter()

    return render(request, 'correlated_plot.html', {'form': form, 'fn':json.dumps(fn),'fp':json.dumps(fp),'tn':json.dumps(tn),'tp':json.dumps(tp)})


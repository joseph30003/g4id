from django.shortcuts import render
from .forms import communityForm
from django.http import HttpResponse
from django.template import loader, Context
import csv
from django.http import StreamingHttpResponse


# Create your views here.

def index(request):
	form = communityForm ()
	return render (request, 'mix.html', {'form': form})


def file_download(request):
	# Create the HttpResponse object with the appropriate CSV header.

	data = request.POST
	community = []
	i = 1
	while 'cname_' + str (i) in data:
		c = {}
		c['name'] = data['cname_' + str (i)]
		c['percentage'] = data['p_' + str (i)]
		community.append (c)
		i += 1

	print (community)

	response = HttpResponse (content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="result.csv"'

	# The data is hard-coded here, but you could load it from a database or
	# some other source.
	csv_data = (
		('First row', 'Foo', 'Bar', 'Baz'),
		('Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"),
	)

	t = loader.get_template ('file_format.txt')
	c = Context ({
		'data': csv_data,
	})
	response.write (t.render (c))
	return response


class Echo (object):
	def write(self, value):
		return value

import os

import random
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
def file_streaming(request):
	data = request.POST
	sum=float(data['sum'])
	community = []
	i = 1
	while 'cname_' + str (i) in data:
		c = {}
		c['path'] = os.path.join(PROJECT_ROOT, "community\\"+data['cname_' + str (i)]+".fq")
		c['number'] = int(float(data['p_' + str (i)])*sum)
		community.append (c)
		i += 1
	print(community)

	response = HttpResponse (content_type="text/plain")
	response['Content-Disposition'] = 'attachment; filename="result.fastq"'
	for c in community:
		fqa = c['path']
		N=c['number']
		records = 0
		for _ in open(fqa):
			records +=1
		records = records/4
		rand_records = sorted ([random.randint (0, records - 1) for _ in range (N)])
		fha=open(fqa)
		rec_no = -1
		written = 0

		for rr in rand_records:
			while rec_no < rr:
				for i in range (4): fha.readline ()

				rec_no += 1
			for i in range (4):
				response.write(fha.readline ())

			rec_no += 1
			written += 1
		assert written == N

	return response

def squ_similarity(candidate,reference):
	c = list(candidate)
	r = list(reference)
	for i in range(0,74):
		if c[i]!=r[i]:
			return False
	return True




def highlight_word(request):
	fn = os.path.join(PROJECT_ROOT, "ref\\Complete_isolates_wo_empty.txt")
	reference = 'atgaagaaggatgatcagattgctgctgctattgctttgagggggatggctaaggatggaaagtttgctgtgaagg'
	types={}
	summary = []
	html = []
	res = {}

	type_i = 0
	sq_rs = []
	with open (fn, 'r') as f:
		cur_sample = ''
		dna = {}
		for line in f:
			line = line.lower ()
			if 'sample' in line:
				if cur_sample:
					res[cur_sample] = dna
				cur_sample = line.strip ('\n').split (' ')[1]
				dna = {}
				continue
			if 'dna:' in line:
				d = line.strip ('\n').split (':')[1]
				if 'n' in d:
					continue
				dna[d] = dna.setdefault (d, 0) + 1


	for key in res:
		sq = {}
		isolate={}
		value = res[key]
		isolate['name']=key
		isolate['same']=0
		isolate['type']={}
		sq['isolate'] = key
		sq['qlist'] = []
		for k in value:
			q={}

			q['number'] = value[k]
			q['con'] = k
			if squ_similarity(k,reference):
				q['same'] =True

				isolate['same'] = isolate['same']+value[k]
			else:
				q['same'] = False
				k_75 = k[0:74]
				if k_75 in types:
					try:
						isolate['type'][types[str (k_75)]] = value[k]
					except KeyError:
						isolate['type'][types[str (k_75)]] = isolate['type'][types[str (k_75)]]+value[k]
				else:
					types[k_75] = type_i
					try:
						isolate['type'][type_i] = value[k]
					except KeyError:
						isolate['type'][type_i] = isolate['type'][type_i]+value[k]

					type_i = type_i + 1

			sq['qlist'].append(q)
		sq_rs.append(sq)
		summary.append(isolate)



	return render (request, 'highlight.html',{'sq':sq_rs,'types':types,'summary':summary,'ref':reference})
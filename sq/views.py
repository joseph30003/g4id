from django.shortcuts import render
from .forms import FileForm
from django.contrib import messages
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
# Create your views here.

def index(request):

	return render (request, 'index.html')


def squ_similarity(candidate,reference):
	if len(reference) > 74:
		leng = 75
	else:
		leng = len(reference)
	c = list(candidate)
	r = list(reference)
	rs = True
	for i in range(0,leng):
		if c[i]==r[i]:
			continue
		else:
			rs = False
			break
	return rs

def pattern_generator(isolate):
	p=[]
	if bool(isolate['same']):
		p.append(str(isolate['same'])+'R')

	for key, value in isolate['type'].items ():
		p.append(str (value) + 'T' + str (key))

	return " ".join(p)

def pattern_number(isolates):
	p_list = []
	for i in isolates:
		p = pattern_generator(i)
		p_list.append(p)


	p_set = set(pt for pt in p_list)
	p_summary = {el:p_list.count(el) for el in p_set}
	return p_summary

def DNA_translate(value):
	coding_dna = Seq(value,generic_dna)
	return coding_dna.translate()


def aa(request):
	res = {}
	reference = 'atgaagaaggatgatcagattgctgctgctattgctttgagggggatggctaaggatggaaagtttgctgtgaagg'
	reference_aa = str(DNA_translate(reference))
	msg = "Please upload file on the right side!"
	types = {}
	same_count=0
	summary = []
	type_i = 1
	sq_rs = []
	pattern_sum = {}
	ps_single = {}
	if request.method == 'POST':

		form = FileForm(request.POST,request.FILES)
		if form.is_valid ():
			msg=""
			#reference = request.POST['reference']
			for chunk in request.FILES['file'].chunks ():
				cur_sample = ''
				dna = {}

				for line in chunk.decode ('utf-8').splitlines ():
					

					if 'Sample' in line:
						if cur_sample:
							res[cur_sample] = dna

						cur_sample = line.strip ('\n').split (' ')[1]
						dna = {}

						continue
					if 'DNA:' in line:
						line = line.lower ()
						d = line.strip ('\n').split (':')[1]
						if 'n' in d or len(d) < 75:
							continue
						dna[d] = dna.setdefault (d, 0) + 1
				res[cur_sample] = dna
		else:
			messages.error(request,'ERROR')


		for key in res:
			sq = {}
			isolate = {}
			value = res[key]

			isolate['name'] = key
			isolate['same'] = 0
			isolate['type'] = {}
			sq['isolate'] = key
			sq['qlist'] = {}
			for k in value:
				k_aa = str(DNA_translate(k))

				if squ_similarity (k_aa, reference_aa):

					same_count = same_count+value[k]
					isolate['same'] = isolate['same'] + value[k]
					if 0 in sq['qlist']:
						sq['qlist'][0]['number'] = isolate['same']
					else:
						sq['qlist'][0] = {}
						sq['qlist'][0]['con'] = k_aa
						sq['qlist'][0]['number'] = isolate['same']
				else:

					if k_aa in types:
						t = types.get(k_aa)
						type_num = t['index']
						t['count'] = t['count'] + 1

					else:
						types[k_aa] = {}
						types[k_aa]['index'] = type_i
						types[k_aa]['count'] = 1

						type_num = type_i
						type_i = type_i + 1

					if type_num in isolate['type']:
						isolate['type'][type_num] = isolate['type'].get(type_num) + value[k]
					else:
						isolate['type'][type_num] = value[k]

					if type_num in sq['qlist']:
						sq['qlist'][type_num]['number'] = isolate['type'][type_num]
					else:
						sq['qlist'][type_num] = {}
						sq['qlist'][type_num]['con'] = k_aa
						sq['qlist'][type_num]['number'] = isolate['type'][type_num]


			sq_rs.append(sq)
			isolate['pattern']=pattern_generator(isolate)
			summary.append (isolate)
		types[reference_aa] = {}
		types[reference_aa]['index'] = 0
		types[reference_aa]['count'] = same_count

		pattern_sum = pattern_number(summary)

		for key,value in pattern_sum.items():
			if " " not in key and len(key) > 0:
				ps_single[key] = value



	else:
		form = FileForm()

	return render (request, 'aasq.html',{'form':form,'sq':sq_rs,'types':types,'summary':summary,
		'pattern_summary':pattern_sum,'pattern_single':ps_single,'ref':reference,'ref_aa':reference_aa,'msg':msg})


def nt(request):
	res = {}
	reference = 'atgaagaaggatgatcagattgctgctgctattgctttgagggggatggctaaggatggaaagtttgctgtgaagg'
	msg = "Please upload file on the right side!"
	types = {}
	same_count = 0
	summary = []
	type_i = 1
	sq_rs = []
	if request.method == 'POST':

		form = FileForm (request.POST, request.FILES)
		if form.is_valid ():
			msg = ""
			# reference = request.POST['reference']
			for chunk in request.FILES['file'].chunks ():
				cur_sample = ''
				dna = {}

				for line in chunk.decode ('utf-8').splitlines ():

					if 'Sample' in line:
						if cur_sample:
							res[cur_sample] = dna
						cur_sample = line.strip ('\n').split (' ')[1]
						dna = {}
						continue
					if 'DNA:' in line:
						line = line.lower ()
						d = line.strip ('\n').split (':')[1]
						if 'n' in d or len (d) < 75:
							continue
						dna[d] = dna.setdefault (d, 0) + 1
		else:
			messages.error (request, 'ERROR')

		for key in res:
			sq = {}
			isolate = {}
			value = res[key]

			isolate['name'] = key
			isolate['same'] = 0
			isolate['type'] = {}
			sq['isolate'] = key
			sq['qlist'] = {}
			for k in value:

				if squ_similarity (k, reference):

					same_count = same_count + value[k]
					isolate['same'] = isolate['same'] + value[k]

					if 0 in sq['qlist']:
						sq['qlist'][0]['number'] = isolate['same']
					else:
						sq['qlist'][0] = {}
						sq['qlist'][0]['con'] = reference
						sq['qlist'][0]['aa'] = DNA_translate(reference)
						sq['qlist'][0]['number'] = isolate['same']
				else:

					k_75 = k[0:75]

					if k_75 in types:
						t = types.get (k_75)
						type_num = t['index']
						t['count'] = t['count'] + 1

					else:
						types[k_75] = {}
						types[k_75]['index'] = type_i
						types[k_75]['count'] = 1
						types[k_75]['translate'] = DNA_translate (k_75)
						type_num = type_i
						type_i = type_i + 1

					if type_num in isolate['type']:
						isolate['type'][type_num] = isolate['type'].get (type_num) + value[k]
					else:
						isolate['type'][type_num] = value[k]

					if type_num in sq['qlist']:
						sq['qlist'][type_num]['number'] = isolate['type'][type_num]
					else:
						sq['qlist'][type_num] = {}
						sq['qlist'][type_num]['con'] = k_75
						sq['qlist'][type_num]['aa'] = DNA_translate(k_75)
						sq['qlist'][type_num]['number'] = isolate['type'][type_num]



			isolate['pattern'] = pattern_generator (isolate)
			summary.append (isolate)
			sq_rs.append(sq)
		types[reference] = {}
		types[reference]['index'] = 0
		types[reference]['count'] = same_count
		types[reference]['translate'] = DNA_translate (reference)
	else:
		form = FileForm ()

	return render (request, 'ntsq.html', {'form': form, 'sq': sq_rs, 'types': types, 'summary': summary,
	                                       'pattern_summary': pattern_number (summary), 'ref': reference[0:75], 'msg': msg})
import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
def aa_final(request):
	fn = os.path.join (PROJECT_ROOT, "ref/Final_isolates.txt")
	res = {}
	reference = 'atgaagaaggatgatcagattgctgctgctattgctttgagggggatggctaaggatggaaagtttgctgtgaagg'
	reference_aa = str (DNA_translate (reference))
	form = ""
	types = {}
	same_count = 0
	summary = []
	type_i = 1
	sq_rs = []
	pattern_sum = {}
	ps_single = {}
	msg = ""
	with open (fn, 'r') as f:
		cur_sample = ''
		dna = {}

		for line in f:

			if 'Sample' in line:
				if cur_sample:
					res[cur_sample] = dna

				cur_sample = line.strip ('\n').split (' ')[1]
				dna = {}

				continue
			if 'DNA:' in line:
				line = line.lower ()
				d = line.strip ('\n').split (':')[1]
				if 'n' in d or len (d) < 75:
					continue
				dna[d] = dna.setdefault (d, 0) + 1
		res[cur_sample] = dna

	for key in res:
		sq = {}
		isolate = {}
		value = res[key]

		isolate['name'] = key
		isolate['same'] = 0
		isolate['type'] = {}
		sq['isolate'] = key
		sq['qlist'] = {}
		for k in value:
			k_aa = str (DNA_translate (k))

			if squ_similarity (k_aa, reference_aa):

				same_count = same_count + value[k]
				isolate['same'] = isolate['same'] + value[k]
				if 0 in sq['qlist']:
					sq['qlist'][0]['number'] = isolate['same']
				else:
					sq['qlist'][0] = {}
					sq['qlist'][0]['con'] = k_aa
					sq['qlist'][0]['number'] = isolate['same']
			else:

				if k_aa in types:
					t = types.get (k_aa)
					type_num = t['index']
					t['count'] = t['count'] + 1

				else:
					types[k_aa] = {}
					types[k_aa]['index'] = type_i
					types[k_aa]['count'] = 1

					type_num = type_i
					type_i = type_i + 1

				if type_num in isolate['type']:
					isolate['type'][type_num] = isolate['type'].get (type_num) + value[k]
				else:
					isolate['type'][type_num] = value[k]

				if type_num in sq['qlist']:
					sq['qlist'][type_num]['number'] = isolate['type'][type_num]
				else:
					sq['qlist'][type_num] = {}
					sq['qlist'][type_num]['con'] = k_aa
					sq['qlist'][type_num]['number'] = isolate['type'][type_num]

		sq_rs.append (sq)
		isolate['pattern'] = pattern_generator (isolate)
		summary.append (isolate)

	types[reference_aa] = {}
	types[reference_aa]['index'] = 0
	types[reference_aa]['count'] = same_count

	pattern_sum = pattern_number (summary)



	for key, value in pattern_sum.items ():
		if " " not in key and len (key) > 0:
			ps_single[key] = value




	return render (request, 'aasq_static.html', {'form':form,'sq': sq_rs, 'types': types, 'summary': summary,
	                                      'pattern_summary': pattern_sum, 'pattern_single': ps_single, 'ref': reference,
	                                      'ref_aa': reference_aa, 'msg': msg})

def aa_com(request):
	fn = os.path.join (PROJECT_ROOT, "ref/Complete_isolates_wo_empty.txt")
	res = {}
	reference = 'atgaagaaggatgatcagattgctgctgctattgctttgagggggatggctaaggatggaaagtttgctgtgaagg'
	reference_aa = str (DNA_translate (reference))
	form = ""
	types = {}
	same_count = 0
	summary = []
	type_i = 1
	sq_rs = []
	pattern_sum = {}
	ps_single = {}
	msg = ""
	with open (fn, 'r') as f:
		cur_sample = ''
		dna = {}

		for line in f:

			if 'Sample' in line:
				if cur_sample:
					res[cur_sample] = dna

				cur_sample = line.strip ('\n').split (' ')[1]
				dna = {}

				continue
			if 'DNA:' in line:
				line = line.lower ()
				d = line.strip ('\n').split (':')[1]
				if 'n' in d or len (d) < 75:
					continue
				dna[d] = dna.setdefault (d, 0) + 1
		res[cur_sample] = dna

	for key in res:
		sq = {}
		isolate = {}
		value = res[key]

		isolate['name'] = key
		isolate['same'] = 0
		isolate['type'] = {}
		sq['isolate'] = key
		sq['qlist'] = {}
		for k in value:
			k_aa = str (DNA_translate (k))

			if squ_similarity (k_aa, reference_aa):

				same_count = same_count + value[k]
				isolate['same'] = isolate['same'] + value[k]
				if 0 in sq['qlist']:
					sq['qlist'][0]['number'] = isolate['same']
				else:
					sq['qlist'][0] = {}
					sq['qlist'][0]['con'] = k_aa
					sq['qlist'][0]['number'] = isolate['same']
			else:

				if k_aa in types:
					t = types.get (k_aa)
					type_num = t['index']
					t['count'] = t['count'] + 1

				else:
					types[k_aa] = {}
					types[k_aa]['index'] = type_i
					types[k_aa]['count'] = 1

					type_num = type_i
					type_i = type_i + 1

				if type_num in isolate['type']:
					isolate['type'][type_num] = isolate['type'].get (type_num) + value[k]
				else:
					isolate['type'][type_num] = value[k]

				if type_num in sq['qlist']:
					sq['qlist'][type_num]['number'] = isolate['type'][type_num]
				else:
					sq['qlist'][type_num] = {}
					sq['qlist'][type_num]['con'] = k_aa
					sq['qlist'][type_num]['number'] = isolate['type'][type_num]

		sq_rs.append (sq)
		isolate['pattern'] = pattern_generator (isolate)
		summary.append (isolate)

	types[reference_aa] = {}
	types[reference_aa]['index'] = 0
	types[reference_aa]['count'] = same_count

	pattern_sum = pattern_number (summary)



	for key, value in pattern_sum.items ():
		if " " not in key and len (key) > 0:
			ps_single[key] = value




	return render (request, 'aasq_static.html', {'form':form,'sq': sq_rs, 'types': types, 'summary': summary,
	                                      'pattern_summary': pattern_sum, 'pattern_single': ps_single, 'ref': reference,
	                                      'ref_aa': reference_aa, 'msg': msg})

def aa_part(request):
	fn = os.path.join (PROJECT_ROOT, "ref/Partial_isolates_wo_empty.txt")
	res = {}
	reference = 'atgaagaaggatgatcagattgctgctgctattgctttgagggggatggctaaggatggaaagtttgctgtgaagg'
	reference_aa = str (DNA_translate (reference))
	form = ""
	types = {}
	same_count = 0
	summary = []
	type_i = 1
	sq_rs = []
	pattern_sum = {}
	ps_single = {}
	msg = ""
	with open (fn, 'r') as f:
		cur_sample = ''
		dna = {}

		for line in f:

			if 'Sample' in line:
				if cur_sample:
					res[cur_sample] = dna

				cur_sample = line.strip ('\n').split (' ')[1]
				dna = {}

				continue
			if 'DNA:' in line:
				line = line.lower ()
				d = line.strip ('\n').split (':')[1]
				if 'n' in d or len (d) < 75:
					continue
				dna[d] = dna.setdefault (d, 0) + 1
		res[cur_sample] = dna

	for key in res:
		sq = {}
		isolate = {}
		value = res[key]

		isolate['name'] = key
		isolate['same'] = 0
		isolate['type'] = {}
		sq['isolate'] = key
		sq['qlist'] = {}
		for k in value:
			k_aa = str (DNA_translate (k))

			if squ_similarity (k_aa, reference_aa):

				same_count = same_count + value[k]
				isolate['same'] = isolate['same'] + value[k]
				if 0 in sq['qlist']:
					sq['qlist'][0]['number'] = isolate['same']
				else:
					sq['qlist'][0] = {}
					sq['qlist'][0]['con'] = k_aa
					sq['qlist'][0]['number'] = isolate['same']
			else:

				if k_aa in types:
					t = types.get (k_aa)
					type_num = t['index']
					t['count'] = t['count'] + 1

				else:
					types[k_aa] = {}
					types[k_aa]['index'] = type_i
					types[k_aa]['count'] = 1

					type_num = type_i
					type_i = type_i + 1

				if type_num in isolate['type']:
					isolate['type'][type_num] = isolate['type'].get (type_num) + value[k]
				else:
					isolate['type'][type_num] = value[k]

				if type_num in sq['qlist']:
					sq['qlist'][type_num]['number'] = isolate['type'][type_num]
				else:
					sq['qlist'][type_num] = {}
					sq['qlist'][type_num]['con'] = k_aa
					sq['qlist'][type_num]['number'] = isolate['type'][type_num]

		sq_rs.append (sq)
		isolate['pattern'] = pattern_generator (isolate)
		summary.append (isolate)

	types[reference_aa] = {}
	types[reference_aa]['index'] = 0
	types[reference_aa]['count'] = same_count

	pattern_sum = pattern_number (summary)



	for key, value in pattern_sum.items ():
		if " " not in key and len (key) > 0:
			ps_single[key] = value




	return render (request, 'aasq_static.html', {'form':form,'sq': sq_rs, 'types': types, 'summary': summary,
	                                      'pattern_summary': pattern_sum, 'pattern_single': ps_single, 'ref': reference,
	                                      'ref_aa': reference_aa, 'msg': msg})
from django import template
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna

register = template.Library()
@register.simple_tag()
def def_highlight(candidate,reference):

	c = list (candidate)
	len = c.__len__ ()

	r = list (reference)
	line = ""
	for i in range (0, 75):
		if c[i] == r[i]:
			line = line + c[i]
		else:
			line = line + "<span style=\"color:red\">" + c[i] + "</span>"


	return line
@register.filter(name = 'get_num')
def get_num(value):

	return value.__len__()

@register.filter(name = 'get_sum')
def get_sum(value):
	sum = 0
	for key,va in value.items():
		sum = sum + va
	return sum

@register.filter(name = 'pattern')
def pattern(value):
	if value:
		return value
	else:
		return "no qualified"

def DNA_translate(value):
	coding_dna = Seq(value,generic_dna)
	return coding_dna.translate()

@register.simple_tag()
def DNA_highlight(candidate,reference):

	ref = str(DNA_translate(reference))

	c = list (str(candidate))
	leng = c.__len__ ()

	r = list (ref)
	line = ""
	for i in range (0, leng):
		if c[i] == r[i]:
			line = line + c[i]
		else:
			line = line + "<span style=\"color:red\">" + c[i] + "</span>"

	return line

@register.simple_tag()
def same_num(value):
	count=0
	for q in value:
		if q['same']:
			count = count + q['number']

	return count
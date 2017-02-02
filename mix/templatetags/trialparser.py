from django import template


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
	if len > 75:
		for i in range (76, len ):
			line = line + c[i]
	return line
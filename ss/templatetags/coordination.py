from django import template

register = template.Library()
@register.filter()
def name_coordination(value):
	return value['cy']+value['r']+10

@register.filter()
def max_height(value):
	if value:
		cy = [l['cy'] for l in value]
		return max(cy)+30
	else:
		return 30

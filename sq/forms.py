from django import forms

class FileForm (forms.Form):
	#reference = forms.CharField(label='ref', max_length=100)
	file = forms.FileField(label='Input File')
	'''
	def is_valid(self):
		valid = super(FileForm,self).is_valid()
		if not valid:
			return valid
		if len(self.cleaned_data['reference']) < 75:
			self._errors['reference'] = [u' the length of reference is less than 75']
			return False
		return True
	'''
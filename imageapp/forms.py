# https://itc.tokyo/django/formview/
from django import forms

class CornerForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['coord_list'].widget = forms.HiddenInput()
		self.fields['submit_btn'].widget = forms.CharField()
		for field in self.base_fields.values():
			field.widget.attrs["class"] = "form-control"
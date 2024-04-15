from django import forms


class RelatorioForm(forms.Form):
    date_start = forms.DateField(widget=forms.DateInput(format=["%Y-%m-%d"]))
    date_end = forms.DateField(widget=forms.DateInput(format=["%Y-%m-%d"]))
    full_operations = forms.ChoiceField(choices=[('1', '1'), ('0', '0')], widget=forms.RadioSelect)

   
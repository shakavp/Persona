from django import forms
from persona_fusion.models import Persona


class PersonaFusionForm(forms.Form):
    persona1 = forms.ModelChoiceField(queryset=Persona.objects.all().order_by('name'), required=True, label=u"Persona 1")
    persona2 = forms.ModelChoiceField(queryset=Persona.objects.all().order_by('name'), required=True, label=u"Persona 2")
    persona3 = forms.ModelChoiceField(queryset=Persona.objects.all().order_by('name'), required=False, label=u"Persona 3")

    # Next Phase
    # persona4 = forms.ModelChoiceField(queryset=Persona.objects.all().order_by('name'), label=u"Persona 4")

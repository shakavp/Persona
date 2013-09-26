from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from persona_fusion.models import Persona
from persona_fusion.forms import PersonaFusionForm
from persona_fusion.operations.fusion import fusion_persona, init_dicts

init_dicts()

def index(request):
    form = PersonaFusionForm()
    result = '---'
    return render_to_response('index.html', {'form': form, 'result': result}, RequestContext(request))


def fusion(name1, name2, name3):
    persona1 = Persona.objects.get(name=name1)
    persona1_tuple = tuple((persona1.name, persona1.arcana, persona1.level))
    persona2 = Persona.objects.get(name=name2)
    persona2_tuple = tuple((persona2.name, persona2.arcana, persona2.level))
    if name3:
        persona3 = Persona.objects.get(name=name3)
        persona3_tuple = tuple((persona3.name, persona3.arcana, persona3.level))
    else:
        persona3 = None
    return fusion_persona(persona1, persona2, persona3)[0]


def calculate(request):
    if request.method == 'POST':
        form = PersonaFusionForm(request.POST)
        if form.is_valid():
            persona1 = Persona.objects.get(pk=int(request.POST['persona1'])).name
            persona2 = Persona.objects.get(pk=int(request.POST['persona2'])).name
            try:
                persona3 = Persona.objects.get(pk=int(request.POST['persona3'])).name
            except ValueError:
                persona3 = None
            result = fusion(persona1, persona2, persona3)
            return render_to_response('index.html', {'form': form, 'result': result}, RequestContext(request))
    return redirect("/persona_fusion/")

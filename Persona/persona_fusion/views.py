from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from persona_fusion.models import Persona
from persona_fusion.forms import PersonaFusionForm


def index(request):
    form = PersonaFusionForm()
    result = '---'
    return render_to_response('index.html', {'form': form, 'result': result}, RequestContext(request))


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
            result = persona1 + persona2 + str(persona3)
            return render_to_response('index.html', {'form': form, 'result': result}, RequestContext(request))
    return redirect("/persona_fusion/")

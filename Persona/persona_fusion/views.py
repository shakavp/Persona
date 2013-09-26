from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse

# from persona_fusion.models import Persona
from persona_fusion.forms import PersonaFusionForm


def index(request):
    form = PersonaFusionForm()
    return render_to_response('index.html', {'form': form}, RequestContext(request))


def calculate(request):
    return HttpResponse("Calculando....")

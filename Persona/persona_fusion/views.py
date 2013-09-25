from django.http import HttpResponse
from persona_fusion.models import Persona


def index(request):
    all_persona = Persona.objects.all()
    output = '; '.join([p.name for p in all_persona])
    return HttpResponse(output)

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from persona_fusion.models import Persona
from persona_fusion.forms import PersonaFusionForm
from persona_fusion.operations.fusion import fusion_persona, init_dicts, fusion_given_a_result

init_dicts()


def index(request):
    form = PersonaFusionForm()
    result = '---'
    return render_to_response('index.html', {'form': form, 'result': result}, RequestContext(request))


def format_persona_formaulas_printing(formula):
    parcels = formula[:-1]
    result = formula[-1]
    return ' + '.join(parcels) + " = " + result


def fusion(name1, name2, name3):
    persona1 = Persona.objects.get(name=name1)
    persona1_tuple = tuple((persona1.name, persona1.arcana, persona1.level))
    persona2 = Persona.objects.get(name=name2)
    persona2_tuple = tuple((persona2.name, persona2.arcana, persona2.level))
    if name3:
        persona3 = Persona.objects.get(name=name3)
        persona3_tuple = tuple((persona3.name, persona3.arcana, persona3.level))
    else:
        persona3_tuple = None
    return fusion_persona(persona1_tuple, persona2_tuple, persona3_tuple)[0]


def calculate(request):
    if request.method == 'POST':
        form = PersonaFusionForm(request.POST)
        if form.is_valid():
            is_result_required = False
            result_found = False
            entry_values = 0

            try:
                persona1 = Persona.objects.get(pk=int(request.POST['persona1'])).name
                entry_values += 1
            except ValueError:
                persona1 = None
                is_result_required = True

            try:
                persona2 = Persona.objects.get(pk=int(request.POST['persona2'])).name
                entry_values += 1
            except ValueError:
                persona2 = None
                is_result_required = True

            try:
                persona3 = Persona.objects.get(pk=int(request.POST['persona3'])).name
                entry_values += 1
            except ValueError:
                persona3 = None

            try:
                persona4 = Persona.objects.get(pk=int(request.POST['persona4'])).name
                result_found = True
            except ValueError:
                persona4 = None

            if is_result_required and not result_found:
                form_error = PersonaFusionForm()
                result_error = "Invalid input"
                return render_to_response('index.html', {'form': form_error, 'result': result_error}, RequestContext(request))

            elif is_result_required and result_found:
                results_list = fusion_given_a_result(persona1, persona2, persona3, persona4)
                [i.insert(2, '') for i in results_list if len(i) == 3]
                return render_to_response('results.html', {'form': form, 'results_list': results_list}, RequestContext(request))

            elif not is_result_required and result_found:
                results_list = fusion_given_a_result(persona1, persona2, persona3, persona4)
                [i.insert(2, '') for i in results_list if len(i) == 3]
                return render_to_response('results.html', {'form': form, 'results_list': results_list}, RequestContext(request))

            else:
                result = fusion(persona1, persona2, persona3)
                mutable = request.POST._mutable
                request.POST._mutable = True
                request.POST['persona4'] = str(Persona.objects.get(name=result).pk)
                request.POST._mutable = mutable
                return render_to_response('index.html', {'form': form, 'result': result}, RequestContext(request))
        else:
            form_error = PersonaFusionForm()
            result_error = "Invalid input"
            return render_to_response('index.html', {'form': form_error, 'result': result_error}, RequestContext(request))
    return redirect("/persona_fusion/")

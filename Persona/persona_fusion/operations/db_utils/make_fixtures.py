from Persona import PERSONAS, is_special_fusion, make_personas_dict


MODEL = '"persona_fusion.Persona"'


def make_json():
    personas_list = open("../personas.txt")
    make_personas_dict(personas_list)
    personas_list.close()
    fixture = open("fixture.json", "w")
    fixture.write("[\n")
    pk = 1
    for arcana, personas_list in PERSONAS.items():
        for persona in personas_list:
            special = is_special_fusion(persona[0])
            fixture.write('    {\n')
            fixture.write('        "model": ' + MODEL + ',\n')
            fixture.write('        "pk": ' + str(pk) + ',\n')
            fixture.write('        "fields": {\n')
            fixture.write('            "name": "' + persona[0] + '",\n')
            fixture.write('            "arcana": "' + arcana + '",\n')
            fixture.write('            "level": ' + str(persona[1]) + ',\n')
            fixture.write('            "price": ' + str(0) + ',\n')
            fixture.write('            "special": "' + str(special) + '"\n')
            fixture.write('        }\n')
            fixture.write('    },\n')
            pk += 1
    fixture.write("]\n")
    fixture.close()
    #print PERSONAS


if __name__ == '__main__':
    make_json()

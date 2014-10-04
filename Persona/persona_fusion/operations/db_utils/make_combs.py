import sys
sys.path.append("..")

from fusion import fusion_persona, init_dicts
import itertools
import json

init_dicts()

PERSONAS = {}


def read_json():
    json_data = open("fixture.json")
    data = json.load(json_data)
    persona_list = [None]
    for item in data:
        name = item['fields']['name']
        arcana = item['fields']['arcana']
        level = item['fields']['level']
        if arcana == "Hanged man":
            arcana = "Hanged Man"
        persona_list.append(tuple((name, arcana, level)))
        PERSONAS.update({item['fields']['name']: item['pk']})
    print persona_list
    json_data.close()
    return persona_list


def format_hex(integer):
    return str(hex(integer)).split('x')[1]


def make_hex_persona_dict():
    hex_file = open("hex.txt", "w")
    json_data = open("fixture.json")
    data = json.load(json_data)
    for item in data:
        hex_file.write(format_hex(item['pk']) + "|")
        hex_file.write(item['fields']['name'] + "\n")
        hex_file.write(item['fields']['name'] + "|")
        hex_file.write(format_hex(item['pk']) + "\n")
    hex_file.close()
    json_data.close()


def make_combinations():
    combs = open("combs.txt", "w")
    persona_list = read_json()
    for subset in itertools.permutations(range(1, len(persona_list)), 2):
        persona_1 = persona_list[subset[0]]
        persona_2 = persona_list[subset[1]]
        result = fusion_persona(persona_1, persona_2)
        if result[0] != 'NA':
            combs.write(format_hex(PERSONAS[persona_list[subset[0]][0]]) + "%")
            combs.write(format_hex(PERSONAS[persona_list[subset[1]][0]]) + "%")
            combs.write("-%")
            combs.write(format_hex(PERSONAS[result[0]]) + "\n")

    for subset in itertools.permutations(range(1, len(persona_list)), 3):
        persona_1 = persona_list[subset[0]]
        persona_2 = persona_list[subset[1]]
        persona_3 = persona_list[subset[2]]
        result = fusion_persona(persona_1, persona_2, persona_3)
        if result[0] != 'NA':
            combs.write(format_hex(PERSONAS[persona_list[subset[0]][0]]) + "%")
            combs.write(format_hex(PERSONAS[persona_list[subset[1]][0]]) + "%")
            combs.write(format_hex(PERSONAS[persona_list[subset[2]][0]]) + "%")
            combs.write(format_hex(PERSONAS[result[0]]) + "\n")

    combs.close()

if __name__ == '__main__':
    #make_combinations()
    make_hex_persona_dict()

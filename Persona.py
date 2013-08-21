#Persona = (str(Nome), str(Arcana), int(Lvl))

DEBUG = False
ARCANAS = {
    1: 'Fool',
    2: 'Magician',
    3: 'Priestess',
    4: 'Empress',
    5: 'Emperor',
    6: 'Hierophant',
    7: 'Lovers',
    8: 'Chariot',
    9: 'Justice',
    10: 'Hermit',
    11: 'Fortune',
    12: 'Strength',
    13: 'Hanged Man',
    14: 'Death',
    15: 'Temperance',
    16: 'Devil',
    17: 'Tower',
    18: 'Star',
    19: 'Moon',
    20: 'Sun',
    21: 'Judgement',
    22: 'Jester',
    23: 'Aeon',
    24: 'World',
    25: 'NA'
}
WEIGHT = {}
FUSION = {}
PERSONAS = {}
SPECIAL_FUSION = {'Alice': ('Nebiros', 'Belial'),
                  'Ardha': ('Parvati', 'Shiva'),
                  'Beelzebub': ('Pazuzu', 'Belphegor', 'Belial', 'Mot', 'Seth', 'Baal Zebul'),
                  'Black Frost': ('Jack Frost', 'Pyro Jack', 'King Frost', 'Pixie', 'Ghoul'),
                  'Futsunushi': ('Ares', 'Triglav', 'Kin-ki', 'Atavaka', 'Neko Shogun'),
                  'Kohryu': ('Gengu', 'Seiryu', 'Suzaku', 'Byakko'),
                  }


def make_weight():
    for i in ARCANAS.items():
        WEIGHT.update({i[1]: i[0]})


def make_combinations():
    combinations = []
    inter_list = [i for i in ARCANAS.values() if i != 'NA' and i != 'World']
    for i in inter_list:
        for j in inter_list:
            combinations.append(tuple((i, j)))
    return combinations


def make_fusion_dict(fusion_list):
    comb_list = make_combinations()
    i = 0
    for line in fusion_list:
        FUSION.update({comb_list[i]: line.strip()})
        i += 1


def file_to_list(personas_list):
    all_file = []
    for line in personas_list:
        all_file.append(line.strip())
    return all_file


def append_persona_to_list(name_lvl, persona_now):
    lvl = name_lvl.pop()
    name = ' '.join(name_lvl)
    PERSONAS[persona_now].append(tuple((name, int(lvl))))


def make_personas_dict(personas_list):
    all_file = file_to_list(personas_list)
    i = 0
    while i < len(all_file):
        persona_now = all_file[i].capitalize()
        PERSONAS.update({persona_now: []})
        i += 1
        while all_file[i]:
            append_persona_to_list(all_file[i].split(' '), persona_now)
            i += 1
            if i == len(all_file):
                break
        i += 1


def find_match_persona(arcana_key, expected_lvl):
    try:
        candidates = PERSONAS[arcana_key]
    except KeyError:
        return tuple(('NA', 0))
    expected_persona = ''
    for persona in candidates:
        if persona[1] < expected_lvl:
            expected_persona = persona
    return expected_persona


def find_result_arcana(arcana_1, arcana_2, result):
    if WEIGHT[arcana_1] > WEIGHT[arcana_2]:
        result[1] = FUSION[(arcana_2, arcana_1)]
    else:
        result[1] = FUSION[(arcana_1, arcana_2)]


def is_normal_same_fusion(arcana_1, arcana_2):
    if arcana_1 == arcana_2:
        return True
    return False


def calculate_result_lvl(persona_1, persona_2):
    fusion_lvl = (persona_1[2] + persona_2[2]) / 2
    if is_normal_same_fusion(persona_1[1], persona_2[1]):
        return fusion_lvl
    return fusion_lvl + 1


def normal_fusion(persona_1, persona_2):
    result = ['', '', 0]
    find_result_arcana(persona_1[1], persona_2[1], result)
    fusion_lvl = calculate_result_lvl(persona_1, persona_2)
    result[0], result[2] = find_match_persona(result[1], int(fusion_lvl))
    return result


def fusion_persona(persona_1, persona_2, persona_3=None):
    if persona_3:
        # TODO
        # result = triangle_fusion(persona_1, persona_2, persona_3)
        return
    else:
        result = normal_fusion(persona_1, persona_2)
    return tuple(result)


def test_fusion_list():
    f1 = open("fusion_list.txt")
    print (WEIGHT)
    for line in f1:
        try:
            WEIGHT[line.strip()]
        except KeyError:
            print ("ERRO:", line.strip())
    f1.close()


def print_debug():
    f1 = open("combina.txt", 'w')
    for l in FUSION.items():
        f1.write(str(l) + '\n')
    test_fusion_list()
    f1.close()
    print (PERSONAS)


if __name__ == '__main__':
    fusion_list = open("fusion_list.txt")
    personas_list = open("personas.txt")
    make_weight()
    make_fusion_dict(fusion_list)
    make_personas_dict(personas_list)
    p1 = ('', 'Lovers', 23)
    p2 = ('', 'Chariot', 23)
    print (fusion_persona(p1, p2))
    print (fusion_persona(p2, p1))
    p1 = ('', 'Star', 23)
    p2 = ('', 'Jester', 23)
    print (fusion_persona(p1, p2))
    print (fusion_persona(p2, p1))
    p1 = ('', 'Strength', 23)
    p2 = ('', 'Judgement', 23)
    print (fusion_persona(p1, p2))
    print (fusion_persona(p2, p1))
    if DEBUG:
        print_debug()
    fusion_list.close()
    personas_list.close()

#Persona = (str(Nome), str(Arcana), int(Lvl))

DEBUG = True
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


def make_weight():
    for i in ARCANAS.items():
        WEIGHT.update({i[1]: i[0]})


def make_combinations():
    combinations = []
    for i in ARCANAS.values():
        for j in ARCANAS.values():
            combinations.append(tuple((i, j)))
    return combinations


def make_fusion_dict(fusion_list):
    comb_list = make_combinations()
    i = 0
    for line in fusion_list:
        FUSION.update({comb_list[i]: line.strip()})
        i += 1


def make_personas_dict(personas_list):
    all_file = []
    for line in personas_list:
        all_file.append(line.strip())
    i = 0
    while i < len(all_file):
        persona_now = all_file[i].lower().capitalize()
        PERSONAS.update({persona_now: []})
        i += 1
        while all_file[i]:
            PERSONAS[persona_now].append(all_file[i])
            i += 1
            if i == len(all_file):
                break
        i += 1
    print PERSONAS


def fusion_persona(persona_1, persona_2, persona_3=None):
    result = ['', '', 0]
    if persona_3:
        return  # TODO
    else:
        if WEIGHT[persona_1[1]] > WEIGHT[persona_2[1]]:
            result[1] = FUSION[(persona_2[1], persona_1[1])]
        else:
            result[1] = FUSION[(persona_1[1], persona_2[1])]
        result[0] = 'Nome'
        result[2] = 100
    return tuple(result)


def test_fusion_list():
    f1 = open("fusion_list.txt")
    print WEIGHT
    for line in f1:
        try:
            WEIGHT[line.strip()]
        except KeyError:
            print "ERRO:", line.strip()
    f1.close()


def print_debug():
    f1 = open("combina.txt", 'w')
    for l in FUSION.items():
        f1.write(str(l) + '\n')
    test_fusion_list()
    f1.close()


if __name__ == '__main__':
    fusion_list = open("fusion_list.txt")
    personas_list = open("personas.txt")
    make_weight()
    make_fusion_dict(fusion_list)
    make_personas_dict(personas_list)
    p1 = ('', 'Lovers', 0)
    p2 = ('', 'Chariot', 0)
    print fusion_persona(p1, p2)
    print fusion_persona(p2, p1)
    if DEBUG:
        print_debug()
    fusion_list.close()
    personas_list.close()

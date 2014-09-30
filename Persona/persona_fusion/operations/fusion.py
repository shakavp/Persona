#Persona = (str(Nome), str(Arcana), int(Lvl))

from operator import itemgetter
from math import ceil


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
                  'Kohryu': ('Genbu', 'Seiryu', 'Suzaku', 'Byakko'),
                  'Lucifer': ('Ananta', 'Anubis', 'Trumpeter', 'Michael', 'Satan', 'Metatron'),
                  'Mahakala': ('Matador', 'White Rider', 'Mother Harlot', 'Daisoujou', 'Hell Biker', 'Trumpeter'),
                  'Neko Shogun': ('Saki Mitama', 'Ara Mitama', 'Kusi Mitama', 'Nigi Mitama'),
                  'Norn': ('Atropos', 'Lachesis', 'Clotho'),
                  'Ongyo-ki': ('Oni', 'Fuu-ki', 'Kin-ki', 'Sui-ki'),
                  'Shiva': ('Rangda', 'Barong'),
                  'Slime': ('Eligor', 'Nata Taishi'),
                  'Tam Lin': ('Phoenix', 'Gdon', 'Yatagarasu', 'Narasimha'),
                  'Trumpeter': ('Matador', 'White Rider', 'Daisoujou', 'Taotie', 'Narasimha'),
                  'Ukobach': ('Lilim', 'Vetala'),
                  'Yatsufusa': ('Makami', 'Orthrus', 'Mothman', 'Thoth', 'Narasimha'),
                  'Yoshitsune': ('Masakado', 'Shiki-Ouji', 'Oukuninushi', 'Hachiman', 'Hitokoto-Nushi')
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


def add_world_arcana():
    arcanas = [i for i in ARCANAS.values() if i != 'NA']
    for arcana in arcanas:
        FUSION.update({tuple(('World', arcana)): 'NA'})
        FUSION.update({tuple((arcana, 'World')): 'NA'})


def add_na_arcana():
    arcanas = [i for i in ARCANAS.values()]
    for arcana in arcanas:
        FUSION.update({tuple(('NA', arcana)): 'NA'})
        FUSION.update({tuple((arcana, 'NA')): 'NA'})


def make_fusion_dict(fusion_list):
    comb_list = make_combinations()
    i = 0
    for line in fusion_list:
        FUSION.update({comb_list[i]: line.strip()})
        i += 1
    add_world_arcana()
    add_na_arcana()


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


def is_special_fusion(persona):
    if persona in SPECIAL_FUSION.keys():
        return True
    return False


def find_lower_persona_exclude_specials(candidates, expected_persona):
    persona_index = len(candidates) - 1
    while persona_index >= 0:
        if not is_special_fusion(candidates[persona_index][0]):
            break
        persona_index -= 1
    return candidates[persona_index]


def find_upper_persona_exclude_specials(candidates, expected_persona):
    persona_index = candidates.index(expected_persona) + 1
    while persona_index < len(candidates):
        if not is_special_fusion(candidates[persona_index][0]):
            break
        persona_index += 1
    if persona_index == len(candidates):
        return candidates[persona_index-1]
    return candidates[persona_index]


def find_persona_exclude_specials(candidates, expected_persona):
    if expected_persona == candidates[-1]:
        return find_lower_persona_exclude_specials(candidates, expected_persona)
    return find_upper_persona_exclude_specials(candidates, expected_persona)


def find_match_persona(arcana_key, expected_lvl):
    try:
        candidates = PERSONAS[arcana_key]
    except KeyError:
        return tuple(('NA', 0))
    expected_persona = candidates[0]
    i = 0
    while i < len(candidates):
        persona = candidates[i]
        if persona[1] < expected_lvl:
            expected_persona = persona
        i += 1
    return find_persona_exclude_specials(candidates, expected_persona)


def find_result_arcana_normal_fusion(arcana_1, arcana_2, result):
    if WEIGHT[arcana_1] > WEIGHT[arcana_2]:
        result[1] = FUSION[(arcana_2, arcana_1)]
    else:
        result[1] = FUSION[(arcana_1, arcana_2)]


def find_result_arcana_triangle_fusion(arcana_1, arcana_2, arcana_3, result):
    find_result_arcana_normal_fusion(arcana_1, arcana_2, result)
    result[1] = FUSION[(result[1], arcana_3)]


def is_normal_same_fusion(arcana_1, arcana_2):
    if arcana_1 == arcana_2:
        return True
    return False


def calculate_result_lvl_normal_fusion(persona_1, persona_2):
    fusion_lvl = (persona_1[2] + persona_2[2]) / 2
    if is_normal_same_fusion(persona_1[1], persona_2[1]):
        return fusion_lvl
    return fusion_lvl + 1


def normal_fusion(persona_1, persona_2):
    result = ['', '', 0]
    find_result_arcana_normal_fusion(persona_1[1], persona_2[1], result)
    fusion_lvl = calculate_result_lvl_normal_fusion(persona_1, persona_2)
    result[0], result[2] = find_match_persona(result[1], int(fusion_lvl))
    return result


def sort_persona_by_level(personas):
    return sorted(personas, key=itemgetter(2))


def calculate_result_lvl_triangle_fusion(persona_1, persona_2, persona_3):
    float_sum = (persona_1[2] + persona_2[2] + persona_3[2])/3.0
    float_sum += 5
    return int(ceil(float_sum))


def triangle_fusion(persona_1, persona_2, persona_3):
    result = ['', '', 0]
    personas = sort_persona_by_level([persona_1, persona_2, persona_3])
    find_result_arcana_triangle_fusion(personas[0][1], personas[1][1],
                                       personas[2][1], result)
    fusion_lvl = calculate_result_lvl_triangle_fusion(persona_1, persona_2,
                                                      persona_3)
    result[0], result[2] = find_match_persona(result[1], int(fusion_lvl))
    return result


def init_dicts():
    fusion_list = open("fusion_list.txt")
    personas_list = open("personas.txt")
    make_weight()
    make_fusion_dict(fusion_list)
    make_personas_dict(personas_list)
    fusion_list.close()
    personas_list.close()


def fusion_persona(persona_1, persona_2, persona_3=None):
    if persona_3:
        result = triangle_fusion(persona_1, persona_2, persona_3)
        return tuple(result)
    result = normal_fusion(persona_1, persona_2)
    return tuple(result)

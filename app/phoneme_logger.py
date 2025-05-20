from utils import normalize_vector
import re

BHAVA_LIST = [
    "Ratiḥ", "Hāsaḥ", "Śokaḥ", "Krodhaḥ", "Utsāhaḥ",
    "Bhayaṁ", "Jugupsā", "Vismayaḥ", "Śamaḥ"
]

BHAVA_VECTORS = {bhava: [1 if i == idx else 0 for i in range(len(BHAVA_LIST))] for idx, bhava in enumerate(BHAVA_LIST)}

PHONEME_CLASS_BHAVA_MAP = {
    "ka": "Utsāhaḥ", "kha": "Utsāhaḥ", "ga": "Utsāhaḥ", "gha": "Utsāhaḥ",
    "cha": "Vismayaḥ", "ja": "Vismayaḥ", "jha": "Vismayaḥ",
    "ṭa": "Krodhaḥ", "ḍa": "Krodhaḥ", "tha": "Krodhaḥ", "dha": "Krodhaḥ",
    "ta": "Śokaḥ", "da": "Śokaḥ", "na": "Śokaḥ", "ṇa": "Śokaḥ",
    "pa": "Bhayaṁ", "pha": "Bhayaṁ", "ba": "Bhayaṁ", "bha": "Bhayaṁ",
    "ma": "Ratiḥ", "ya": "Ratiḥ", "va": "Ratiḥ", "la": "Ratiḥ",
    "śa": "Śamaḥ", "ṣa": "Śamaḥ", "sa": "Śamaḥ", "ha": "Krodhaḥ",
    "ra": "Utsāhaḥ", "ña": "Jugupsā"
}

def get_bhava_vector_with_log(name):
    name = name.lower()
    vector = [0] * len(BHAVA_LIST)
    log = []

    for phoneme, bhava in PHONEME_CLASS_BHAVA_MAP.items():
        if re.search(phoneme, name):
            log.append((phoneme, bhava))
            vector = [v + b for v, b in zip(vector, BHAVA_VECTORS[bhava])]

    vector = normalize_vector(vector)
    return vector, log

def get_dominant_bhava(vector):
    if not vector or max(vector) == 0:
        return "Śamaḥ"
    idx = vector.index(max(vector))
    return BHAVA_LIST[idx]

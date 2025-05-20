PHONEME_BHAVA_MAP = {
    "ra": "Utsāhaḥ",
    "ma": "Ratiḥ",
    "na": "Śokaḥ",
    "ha": "Krodhaḥ",
    "sa": "Śamaḥ",
    "ka": "Vismayaḥ",
    "ga": "Bhayaṁ",
    "ba": "Hāsaḥ",
    "ju": "Jugupsā",
    "vi": "Vismayaḥ"
}

def get_bhava_from_name(name):
    name = name.lower()
    for phoneme, bhava in PHONEME_BHAVA_MAP.items():
        if phoneme in name:
            return bhava
    return "Śamaḥ"  # Default

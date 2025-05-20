from utils import format_name

def suggest_names_for_bhava(bhava):
    bhava_name_map = {
        "Ratiḥ": ["Madhav", "Preeti", "Rama", "Milan"],
        "Hāsaḥ": ["Hasan", "Harsha", "Hasi", "Haasya"],
        "Śokaḥ": ["Shanaya", "Nalin", "Nisha", "Navya"],
        "Krodhaḥ": ["Kiran", "Kartik", "Harshad", "Krodhit"],
        "Utsāhaḥ": ["Utsav", "Ravi", "Raghav", "Ranveer"],
        "Bhayaṁ": ["Bhavna", "Garv", "Gagan", "Bhairav"],
        "Jugupsā": ["Jugnu", "Jugal", "Juhitha", "Jugant"],
        "Vismayaḥ": ["Vishal", "Vikas", "Vaibhav", "Vinay"],
        "Śamaḥ": ["Samir", "Samar", "Sanya", "Shaant"]
    }
    return [format_name(name) for name in bhava_name_map.get(bhava, ["No suggestions available"])]

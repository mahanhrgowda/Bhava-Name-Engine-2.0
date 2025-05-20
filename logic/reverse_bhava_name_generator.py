def suggest_names_for_bhava(bhava):
    # Sample name suggestions based on Bhāva
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
    return bhava_name_map.get(bhava, ["No suggestions available"])

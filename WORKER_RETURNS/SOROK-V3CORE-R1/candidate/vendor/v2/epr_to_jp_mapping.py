"""
EPR to JP (Joshua Project) Mapping for Multiple Countries.

This module provides mappings from EPR ethnic groups to JP people groups.
The mapping is used to sample granular JP groups while maintaining EPR power status.

Countries covered:
- India (comprehensive)
- Indonesia (economical)
- Pakistan (economical)
- Brazil (economical)
- Mexico (economical)
- Ethiopia (economical)
- Thailand (economical)
"""

# EPR Group → JP Group Keywords/Patterns for India
INDIA_EPR_TO_JP_MAPPING = {
    "Scheduled Castes": {
        "keywords": [
            "dalit", "scheduled caste", "sc", "harijan", "chamar", "pasi", 
            "dusadh", "khatik", "valmiki", "mahar", "mang", "ravidas",
            "chuhra", "mehtar", "lal begi", "chohra", "adi dravida", 
            "madiga", "mala", "pulayan", "cheruman"
        ],
        "exclude": ["muslim", "sikh", "christian", "buddhist"]  # Only if these are the primary identifier
    },
    "Scheduled Tribes": {
        "keywords": [
            "scheduled tribe", "st", "adivasi", "tribal", "gond", "santal", 
            "bhil", "munda", "oraon", "ho", "khasi", "garo", "naga", 
            "mizo", "bodo", "tripuri", "manipuri", "meitei"
        ],
        "exclude": []
    },
    "Other Backward Classes/Castes": {
        "keywords": [
            "obc", "other backward", "yadav", "kurmi", "gupta", "patel", 
            "jain", "vaishya", "koli", "patelia", "bhabra", "kunbi", 
            "banjara", "tanti", "rajbansi", "namassej"
        ],
        "exclude": ["scheduled caste", "scheduled tribe", "sc", "st", "dalit", "adivasi"]
    },
    "Other Muslims": {
        "keywords": [
            "muslim", "shaikh", "syed", "sayyid", "pathan", "ansari", "khan", 
            "sheikh", "momin", "memon", "pashtun", "qureshi", "siddiqi", "faruqi"
        ],
        "exclude": ["kashmiri"]  # Kashmiri Muslims are separate
    },
    "Kashmiri Muslims": {
        "keywords": ["kashmiri", "kashmir"],
        "require": ["muslim"]  # Must be Muslim
    },
    "Punjabi-Sikhs (non-SC/ST/OBCs)": {
        "keywords": ["sikh", "punjabi"],
        "exclude": ["scheduled caste", "scheduled tribe", "sc", "st", "obc"]
    },
    "Hindi (Non SC/ST OBCs)": {
        "keywords": ["hindi"],
        "exclude": ["scheduled caste", "scheduled tribe", "sc", "st", "obc", "muslim", "sikh"],
        "also_match": [
            "brahmin", "rajput", "thakur", "kayastha", "baniya", "kshatriya",  # Upper castes
            "jat", "bania", "teli", "kumhar", "mali", "nai", "sonar", "lohar",  # Common castes
            "koiri", "kahar", "gujar", "kachhi", "badhai", "gadaria"  # More castes
        ],
        "match_by_language": "Hindi"  # Also match by language
    },
    "Bengali (non-SC/ST/OBCs)": {
        "keywords": ["bengali", "bangla", "mahishya", "tanti", "rajbansi", "namassej"],  # Major Bengali castes
        "exclude": ["scheduled caste", "scheduled tribe", "sc", "st", "obc", "muslim"],
        "match_by_language": "Bengali"  # Also match by language
    },
    "Tamil (non-SC/ST/OBCs)": {
        "keywords": ["tamil", "vanniyan", "vanniyar"],  # Vanniyan is major Tamil caste
        "exclude": ["scheduled caste", "scheduled tribe", "sc", "st", "obc", "muslim"],
        "match_by_language": "Tamil"  # Also match by language
    },
    "Telugu (Non SC/ST/OBCs)": {
        "keywords": ["telugu", "kapu"],  # Kapu is major Telugu caste
        "exclude": ["scheduled caste", "scheduled tribe", "sc", "st", "obc", "muslim"],
        "match_by_language": "Telugu"  # Also match by language
    },
    "Marathi (non-SC/ST)": {
        "keywords": ["marathi", "mahratta", "mahrata"],
        "exclude": ["scheduled caste", "scheduled tribe", "sc", "st"]
    },
    "Gujarati (non-SC/ST)": {
        "keywords": ["gujarati", "gujarat"],
        "exclude": ["scheduled caste", "scheduled tribe", "sc", "st"]
    },
    "Kannada (non-SC/ST)": {
        "keywords": ["kannada", "kannadiga", "vakkaliga"],  # Vakkaliga is major Kannada caste
        "exclude": ["scheduled caste", "scheduled tribe", "sc", "st"],
        "match_by_language": "Kannada"  # Also match by language
    },
    "Malyalam (non-SC/ST)": {
        "keywords": ["malayalam", "malyalam", "malayali"],
        "exclude": ["scheduled caste", "scheduled tribe", "sc", "st"],
        "match_by_language": "Malayalam"  # Match by primary_language field
    },
    "Oriya (non-SC/ST)": {
        "keywords": ["oriya", "odia", "odisha"],
        "exclude": ["scheduled caste", "scheduled tribe", "sc", "st"]
    },
    "Assamese (non-SC/ST/OBCs)": {
        "keywords": ["assamese", "assam"],
        "exclude": ["scheduled caste", "scheduled tribe", "sc", "st", "obc", "muslim"]
    },
    "Manipuri": {
        "keywords": ["manipuri", "meitei"],
        "exclude": []
    },
    "Naga": {
        "keywords": ["naga"],
        "exclude": ["nagar", "nagara", "nagartha"]  # Exclude non-tribal Nagar groups
    },
    "Bodo": {
        "keywords": ["bodo"],
        "exclude": []
    },
    "Indigenous Tripuri": {
        "keywords": ["tripuri", "tripura"],
        "exclude": [],
        "match_by_language": "Kok Borok"  # Tripuri language - also try "Kokborok"
    },
    "Mizo": {
        "keywords": ["mizo", "lushai"],
        "exclude": []
    }
}


# JP groups to exclude for India (Indonesian/Malaysian/East Timorese - wrong country in JP)
INDIA_NON_NATIVE_EXCLUDE = (
    "javanese", "sundanese", "balinese", "batak", "acehnese", "madurese",
    "minangkabau", "dayak", "makassar", "bugis", "papuan", "ambonese", "minahasa",
    "timorese", "east timor", "ternate", "gorontalo"
)


def get_jp_groups_for_epr(epr_group: str, jp_groups: list) -> list:
    """
    Get all JP groups that match an EPR group.
    
    Args:
        epr_group: EPR group name (e.g., "Scheduled Castes")
        jp_groups: List of JP group dicts with 'people_name' and optionally 'primary_language' keys
    
    Returns:
        List of matching JP group dicts
    """
    if epr_group not in INDIA_EPR_TO_JP_MAPPING:
        return []
    
    mapping = INDIA_EPR_TO_JP_MAPPING[epr_group]
    keywords = mapping.get("keywords", [])
    exclude = list(mapping.get("exclude", [])) + list(INDIA_NON_NATIVE_EXCLUDE)
    require = mapping.get("require", [])
    also_match = mapping.get("also_match", [])
    match_by_language = mapping.get("match_by_language")  # New: match by language field
    
    matching = []
    
    for jp_group in jp_groups:
        jp_name = jp_group.get("people_name", "").lower()
        jp_language = (jp_group.get("primary_language") or "").lower()
        
        # Strategy 1: Match by language (if specified)
        if match_by_language:
            # Try both the exact language name and variations
            lang_variations = [
                match_by_language.lower(),
                match_by_language.lower().replace(" ", ""),  # "kok borok" -> "kokborok"
                match_by_language.lower().replace(" ", "-"),  # "kok borok" -> "kok-borok"
            ]
            lang_match = any(var in jp_language for var in lang_variations)
            if not lang_match:
                continue
        else:
            # Strategy 2: Match by keywords in name
            matches_keyword = any(kw in jp_name for kw in keywords)
            matches_also = any(kw in jp_name for kw in also_match) if also_match else False
            
            if not (matches_keyword or matches_also):
                continue
        
        # Check exclude list
        if exclude and any(ex in jp_name for ex in exclude):
            continue
        
        # Check require list (all must be present)
        if require and not all(req in jp_name for req in require):
            continue
        
        matching.append(jp_group)
    
    return matching


def build_india_epr_to_jp_mapping(jp_groups: list) -> dict:
    """
    Build complete EPR → JP mapping for India.
    
    Args:
        jp_groups: List of all JP groups for India
    
    Returns:
        Dict mapping EPR group name → list of JP group dicts
    """
    epr_groups = list(INDIA_EPR_TO_JP_MAPPING.keys())
    mapping = {}
    
    for epr_group in epr_groups:
        matching_jp = get_jp_groups_for_epr(epr_group, jp_groups)
        mapping[epr_group] = matching_jp
    
    return mapping


# ============================================================================
# INDONESIA MAPPING
# ============================================================================

INDONESIA_EPR_TO_JP_MAPPING = {
    "Javanese": {
        "keywords": ["java", "javanese"],
        "match_by_language": "Javanese"
    },
    "Sundanese": {
        "keywords": ["sunda", "sundanese"],
        "match_by_language": "Sunda"
    },
    "Madura": {
        "keywords": ["madura", "madurese"],
        "match_by_language": "Madura"
    },
    "Minangkabaus": {
        "keywords": ["minang", "minangkabau"],
        "match_by_language": "Minangkabau"
    },
    "Malay": {
        "keywords": ["malay"],
        "exclude": ["pattani"]  # Pattani is Thai Malay
    },
    "Bataks": {
        "keywords": ["batak", "toba", "karo", "simalungun", "mandailing", "pakpak", "angkola"]
    },
    "Chinese (Han)": {
        "keywords": ["chinese", "han"],
        "exclude": ["taiwan"]
    },
    "Dayak": {
        "keywords": ["dayak", "daya"]
    },
    "Acehnese": {
        "keywords": ["aceh", "acehnese"]
    },
    "Balinese": {
        "keywords": ["bali", "balinese"],
        "match_by_language": "Balinese"
    },
    "Makassarese and Bugis": {
        "keywords": ["makassar", "bugis", "buginese"]
    },
    "Papuans": {
        "keywords": ["papua", "papuan"]
    },
    "Minahasa": {
        "keywords": ["minahasa"]
    },
    "Amboinese": {
        "keywords": ["ambon", "amboinese", "ambonese"]
    },
    "Gorontalos": {
        "keywords": ["gorontalo"]
    },
    "Ternate": {
        "keywords": ["ternate"]
    }
}


# ============================================================================
# PAKISTAN MAPPING
# ============================================================================

PAKISTAN_EPR_TO_JP_MAPPING = {
    "Punjabi": {
        "keywords": ["punjabi", "jat", "rajput", "arain", "awan", "gujar", "hajam", "teli", "kumhar"],
        "match_by_language": "Punjabi"
    },
    "Pashtuns": {
        "keywords": ["pashtun", "pathan", "yusafzai"],
        "match_by_language": "Pashto"
    },
    "Sindhi": {
        "keywords": ["sindhi"],
        "match_by_language": "Sindhi"
    },
    "Mohajirs": {
        "keywords": ["mohajir", "urdu"],
        "match_by_language": "Urdu"
    },
    "Baluchis": {
        "keywords": ["baloch", "baluch", "baluchi"],
        "match_by_language": "Balochi"
    },
    "Hindus": {
        "keywords": ["hindu"],
        "exclude": ["sikh", "muslim", "christian"]
    },
    "Christians": {
        "keywords": ["christian"],
        "exclude": ["muslim"]
    },
    "Ahmadis": {
        "keywords": ["ahmadi", "ahmadiyya"]
    }
}


# ============================================================================
# BRAZIL MAPPING
# ============================================================================

BRAZIL_EPR_TO_JP_MAPPING = {
    "Whites": {
        "keywords": ["white", "brazilian, white", "european"],
        "exclude": ["black", "mestizo", "indigenous", "quilombola"]
    },
    "Afrobrazilians": {
        "keywords": ["black", "brazilian, black", "afro", "quilombola"]
    },
    "Indigenous peoples": {
        "keywords": ["indigenous", "ticuna", "guarani", "yanomami", "xingu", "kayapo"]
    }
}


# ============================================================================
# MEXICO MAPPING
# ============================================================================

MEXICO_EPR_TO_JP_MAPPING = {
    "Mestizos": {
        "keywords": ["mexican", "mestizo", "amerindian, detribalized"],
        "exclude": ["maya", "nahuatl", "zapotec", "mixtec", "purepecha", "tzeltal", "tzotzil"]
    },
    "Other indigenous groups": {
        "keywords": ["nahuatl", "zapotec", "mixtec", "purepecha", "tzeltal", "tzotzil", "otomi", "totonac"],
        "exclude": ["maya"]
    },
    "Afromexicans": {
        "keywords": ["afro", "afromexican"]
    },
    "Maya": {
        "keywords": ["maya"]
    }
}


# ============================================================================
# ETHIOPIA MAPPING
# ============================================================================

ETHIOPIA_EPR_TO_JP_MAPPING = {
    "Oroma": {
        "keywords": ["oromo", "oroma"],
        "match_by_language": "Oromo"
    },
    "Amhara": {
        "keywords": ["amhara", "amharic"],
        "match_by_language": "Amharic"
    },
    "Other Southern Nations": {
        "keywords": ["sidama", "wolaitta", "gurage", "gamo", "gofa", "hadiyya", "kambaata"],
        "exclude": ["oromo", "amhara", "tigray", "somali", "afar"]
    },
    "Somali (Ogaden)": {
        "keywords": ["somali"],
        "match_by_language": "Somali"
    },
    "Tigry": {
        "keywords": ["tigray", "tigrinya", "tigry"],
        "match_by_language": "Tigrigna"
    },
    "Sidama": {
        "keywords": ["sidama"],
        "match_by_language": "Sidaama"
    },
    "Afar": {
        "keywords": ["afar"],
        "match_by_language": "Afar"
    },
    "Beni-Shugal-Gumez": {
        "keywords": ["beni", "shugal", "gumez", "gumuz"]
    },
    "Anuak": {
        "keywords": ["anuak"]
    },
    "Harari": {
        "keywords": ["harari", "harer"]
    }
}


# ============================================================================
# THAILAND MAPPING
# ============================================================================

THAILAND_EPR_TO_JP_MAPPING = {
    "Thai": {
        "keywords": ["thai"],
        "exclude": ["chinese", "malay", "khmer", "hill", "shan"],
        "match_by_language": "Thai"
    },
    "Chinese": {
        "keywords": ["chinese"],
        "exclude": ["thai"]
    },
    "Malay Muslims": {
        "keywords": ["malay", "pattani"],
        "require": ["muslim"]  # Must be Muslim
    },
    "Hill Tribes": {
        "keywords": ["hill", "karen", "hmong", "lahu", "akha", "lisu", "yao", "mien"]
    },
    "Shan": {
        "keywords": ["shan"]
    }
}


# ============================================================================
# GENERIC MAPPING FUNCTION
# ============================================================================

def get_jp_groups_for_epr_generic(epr_group: str, jp_groups: list, country_mapping: dict) -> list:
    """
    Generic function to get JP groups for an EPR group using a country-specific mapping.
    
    Args:
        epr_group: EPR group name
        jp_groups: List of JP group dicts
        country_mapping: Country-specific mapping dict (e.g., INDONESIA_EPR_TO_JP_MAPPING)
    
    Returns:
        List of matching JP group dicts
    """
    if epr_group not in country_mapping:
        return []
    
    mapping = country_mapping[epr_group]
    keywords = mapping.get("keywords", [])
    exclude = mapping.get("exclude", [])
    require = mapping.get("require", [])
    match_by_language = mapping.get("match_by_language")
    
    matching = []
    
    for jp_group in jp_groups:
        jp_name = jp_group.get("people_name", "").lower()
        jp_language = (jp_group.get("primary_language") or "").lower()
        
        # Strategy 1: Match by language (if specified)
        if match_by_language:
            lang_variations = [
                match_by_language.lower(),
                match_by_language.lower().replace(" ", ""),
                match_by_language.lower().replace(" ", "-"),
            ]
            lang_match = any(var in jp_language for var in lang_variations)
            if not lang_match:
                continue
        else:
            # Strategy 2: Match by keywords in name
            matches_keyword = any(kw in jp_name for kw in keywords)
            if not matches_keyword:
                continue
        
        # Check exclude list
        if exclude and any(ex in jp_name for ex in exclude):
            continue
        
        # Check require list (all must be present)
        if require and not all(req in jp_name for req in require):
            continue
        
        matching.append(jp_group)
    
    return matching


# ============================================================================
# KENYA MAPPING
# ============================================================================

KENYA_EPR_TO_JP_MAPPING = {
    "Kikuyu-Meru-Emb": {
        "keywords": ["kikuyu", "meru", "embu"],
        "match_by_language": "Gikuyu"
    },
    "Kalenjin-Masai-Turkana-Samburu": {
        "keywords": ["kalenjin", "masai", "maasai", "turkana", "samburu", "kipsigis", "nandi"],
        "match_by_language": "Kipsigis"
    },
    "Luhya": {
        "keywords": ["luhya", "bukusu"],
        "match_by_language": "Bukusu"
    },
    "Luo": {
        "keywords": ["luo"],
        "match_by_language": "Dholuo"
    },
    "Kamba": {
        "keywords": ["kamba"],
        "match_by_language": "Kamba"
    },
    "Kisii": {
        "keywords": ["kisii", "gusii"],
        "match_by_language": "Ekegusii"
    },
    "Mijikenda": {
        "keywords": ["mijikenda", "giriama", "digo", "duruma"],
        "match_by_language": "Kigiryama"
    },
    "Somali": {
        "keywords": ["somali"],
        "match_by_language": "Somali"
    }
}


# ============================================================================
# MALAYSIA MAPPING
# ============================================================================

MALAYSIA_EPR_TO_JP_MAPPING = {
    "Malays": {
        "keywords": ["malay"],
        "exclude": ["chinese", "indian", "dayak", "kadazan", "iban"],
        "match_by_language": "Malay"
    },
    "Chinese": {
        "keywords": ["chinese", "han"],
        "exclude": ["malay", "indian"]
    },
    "East Indians": {
        "keywords": ["indian", "tamil", "malayali", "telugu"],
        "exclude": ["chinese", "malay"]
    },
    "Dayaks": {
        "keywords": ["dayak", "iban"],
        "match_by_language": "Iban"
    },
    "Kadazans": {
        "keywords": ["kadazan", "dusun"],
        "match_by_language": "Kadazan Dusun"
    },
    "Orang Asli": {
        "keywords": ["orang asli", "semai", "temiar", "jakun"]
    }
}


# ============================================================================
# NEPAL MAPPING
# ============================================================================

NEPAL_EPR_TO_JP_MAPPING = {
    "Caste Hill Hindu Elite": {
        "keywords": ["chhetri", "brahmin", "hill brahmin"],
        "exclude": ["dalit", "tharu", "magar", "tamang", "newar", "rai", "gurung", "limbu"]
    },
    "Adibasi Janajati": {
        "keywords": ["tharu", "magar", "tamang", "rai", "gurung", "limbu", "sherpa", "yakthumba"],
        "exclude": ["brahmin", "chhetri", "dalit"]
    },
    "Dalits": {
        "keywords": ["dalit", "kami", "sarki", "damai"],
        "exclude": ["brahmin", "chhetri"]
    },
    "Madhesi": {
        "keywords": ["madhesi", "maithili", "bhojpuri"],
        "exclude": ["brahmin", "chhetri"]
    },
    "Newars": {
        "keywords": ["newar", "newah"],
        "match_by_language": "Newar"
    },
    "Muslims": {
        "keywords": ["muslim", "islam"],
        "exclude": ["hindu", "buddhist", "christian"]
    }
}


# ============================================================================
# GHANA MAPPING
# ============================================================================

GHANA_EPR_TO_JP_MAPPING = {
    "Other Akans": {
        "keywords": ["akan", "fante", "akyem", "brong", "abron"],
        "exclude": ["asante", "ewe", "ga", "dagomba"],
        "match_by_language": "Akan"
    },
    "Northern Groups (Mole-Dagbani, Gurma, Grusi)": {
        "keywords": ["dagomba", "dagaaba", "konkomba", "mamprusi", "dagaare"],
        "match_by_language": "Dagbani"
    },
    "Asante (Akan)": {
        "keywords": ["asante", "ashanti"],
        "match_by_language": "Akan"
    },
    "Ewe": {
        "keywords": ["ewe"],
        "match_by_language": "Ewe"
    },
    "Ga-Adangbe": {
        "keywords": ["ga", "adangbe", "dangme"],
        "match_by_language": "Ga"
    }
}


# ============================================================================
# UGANDA MAPPING
# ============================================================================

UGANDA_EPR_TO_JP_MAPPING = {
    "Baganda": {
        "keywords": ["baganda", "ganda"],
        "match_by_language": "Ganda"
    },
    "South-Westerners (Ankole, Banyoro, Toro)": {
        "keywords": ["banyankore", "ankole", "banyoro", "toro", "bakiga", "nyankore"],
        "match_by_language": "Nyankore"
    },
    "Langi/Acholi": {
        "keywords": ["lango", "acholi", "langi"],
        "match_by_language": "Acholi"
    },
    "Basoga": {
        "keywords": ["soga", "basoga"],
        "match_by_language": "Soga"
    },
    "Teso": {
        "keywords": ["teso", "iteso"],
        "match_by_language": "Ateso"
    },
    "Far North-West Nile (Kakwa-Nubian, Madi, Lugbara, Alur)": {
        "keywords": ["lugbara", "madi", "alur", "kakwa", "nubian"]
    },
    "Banyarwanda": {
        "keywords": ["banyarwanda", "rwanda", "ruanda"]
    },
    "Karamojong": {
        "keywords": ["karamojong", "karimojong", "karamoja"]
    },
    "Asians": {
        "keywords": ["asian", "indian", "pakistani", "bangladeshi"]
    }
}


# ============================================================================
# CAMEROON MAPPING
# ============================================================================

CAMEROON_EPR_TO_JP_MAPPING = {
    "Bamileke": {
        "keywords": ["bamileke", "ghomala", "yemba"],
        "match_by_language": "Ghomala"
    },
    "Beti (and related peoples)": {
        "keywords": ["beti", "ewondo", "bulu", "fang"],
        "match_by_language": "Ewondo"
    },
    "Fulani (and other northern Muslim peoples)": {
        "keywords": ["fulani", "fulfulde"],
        "match_by_language": "Fulfulde"
    },
    "Northwestern Anglophones (Grassfielders)": {
        "keywords": ["bamun", "mum", "grassfield"]
    },
    "Bassa/Duala": {
        "keywords": ["bassa", "duala"]
    },
    "Southwestern Anglophones (Bakweri etc.)": {
        "keywords": ["bakweri", "bafaw"]
    }
}


# ============================================================================
# COLOMBIA MAPPING
# ============================================================================

COLOMBIA_EPR_TO_JP_MAPPING = {
    "Whites/mestizos": {
        "keywords": ["colombian", "mestizo", "white"],
        "exclude": ["afro", "indigenous", "wayuu", "paez", "guajibo"]
    },
    "Afro-Colombian": {
        "keywords": ["afro", "zambo", "mulatto"],
        "exclude": ["indigenous"]
    },
    "Indigenous peoples": {
        "keywords": ["wayuu", "paez", "guajibo", "pijao", "quaiquer", "guambiano", "indigenous"]
    }
}


# ============================================================================
# PERU MAPPING
# ============================================================================

PERU_EPR_TO_JP_MAPPING = {
    "Whites/mestizos": {
        "keywords": ["peruvian"],
        "exclude": ["quechua", "aymara", "indigenous"]
    },
    "Indigenous peoples of the Andes": {
        "keywords": ["quechua", "aymara"],
        "match_by_language": "Quechua"
    },
    "Afroperuvians": {
        "keywords": ["afro"]
    },
    "Indigenous peoples of the Amazon": {
        "keywords": ["shipibo", "ashaninka", "aguaruna"]
    }
}


# ============================================================================
# ARGENTINA MAPPING
# ============================================================================

ARGENTINA_EPR_TO_JP_MAPPING = {
    "Whites/mestizos": {
        "keywords": ["argentinian", "white", "mestizo"],
        "exclude": ["indigenous", "toba", "diaguita", "kolla", "quichua", "guarani"]
    },
    "Indigenous peoples": {
        "keywords": ["toba", "diaguita", "kolla", "quichua", "guarani", "comechingon", "huarpe", "indigenous"]
    }
}


# ============================================================================
# SOUTH AFRICA MAPPING
# ============================================================================

SOUTH_AFRICA_EPR_TO_JP_MAPPING = {
    "Zulu": {
        "keywords": ["zulu"],
        "match_by_language": "Zulu"
    },
    "Xhosa": {
        "keywords": ["xhosa"],
        "match_by_language": "Xhosa"
    },
    "Pedi (North Sotho)": {
        "keywords": ["pedi", "north sotho", "northern sotho"],
        "match_by_language": "Northern Sotho"
    },
    "Afrikaners": {
        "keywords": ["afrikaner", "boer"],
        "match_by_language": "Afrikaans"
    },
    "Coloreds": {
        "keywords": ["colored", "coloured", "cape colored"]
    },
    "South Sotho": {
        "keywords": ["sotho", "south sotho", "southern sotho"],
        "exclude": ["north", "northern", "pedi"],
        "match_by_language": "Southern Sotho"
    },
    "Tswana": {
        "keywords": ["tswana", "tshwana"],
        "match_by_language": "Tswana"
    },
    "English Speakers": {
        "keywords": ["english"],
        "match_by_language": "English"
    },
    "Tsonga": {
        "keywords": ["tsonga"],
        "match_by_language": "Tsonga"
    },
    "Swazi": {
        "keywords": ["swazi", "swati"],
        "match_by_language": "Swati"
    },
    "Venda": {
        "keywords": ["venda"],
        "match_by_language": "Venda"
    },
    "Ndebele": {
        "keywords": ["ndebele"],
        "match_by_language": "Ndebele"
    },
    "Other": {
        "keywords": ["indian", "asian", "chinese"]
    },
    "San": {
        "keywords": ["san", "bushman", "khoisan"]
    }
}


# ============================================================================
# AFGHANISTAN MAPPING
# ============================================================================

AFGHANISTAN_EPR_TO_JP_MAPPING = {
    "Pashtuns": {
        "keywords": ["pashtun", "pathan", "pushtun", "afghan"],
        "exclude": ["tajik", "hazara", "uzbek"],
        "match_by_language": "Pashto"
    },
    "Tajiks": {
        "keywords": ["tajik", "tadzhik", "afghan, tajik"],
        "match_by_language": "Dari"
    },
    "Hazara": {
        "keywords": ["hazara"],
        "match_by_language": "Hazaragi"
    },
    "Uzbeks": {
        "keywords": ["uzbek", "uzbek, southern"],
        "match_by_language": "Uzbek"
    },
    "Aimaq": {
        "keywords": ["aimaq", "aimak"]
    },
    "Turkmen": {
        "keywords": ["turkmen", "turkoman"],
        "match_by_language": "Turkmen"
    },
    "Nuristani": {
        "keywords": ["nuristani"]
    },
    "Qizalbash": {
        "keywords": ["qazilbash", "qizilbash"]
    }
}


# ============================================================================
# LAOS MAPPING
# ============================================================================

LAOS_EPR_TO_JP_MAPPING = {
    "Lao (incl. Phuan)": {
        "keywords": ["lao"],
        "exclude": ["hmong", "khmu", "khamu", "tai", "mien", "lue", "thoeng", "sung", "bru", "laven", "katang", "prai", "mal", "so"],
        "match_by_language": "Lao"
    },
    "Lao Thoeng (excl. Khmou)": {
        "keywords": ["thoeng", "bru", "laven", "katang", "prai", "mal", "so"],
        "exclude": ["khmu", "khamu", "hmong"]
    },
    "Lao Tai": {
        "keywords": ["tai", "thai", "lue", "phu thai"],
        "exclude": ["lao", "hmong"],
        "match_by_language": "Thai"
    },
    "Khmou": {
        "keywords": ["khmu", "khamu"],
        "match_by_language": "Khmu"
    },
    "Hmong": {
        "keywords": ["hmong", "miao"],
        "match_by_language": "Hmong"
    },
    "Lao Sung (excl. Hmong)": {
        "keywords": ["sung", "mien", "yao"],
        "exclude": ["hmong"],
        "match_by_language": "Mien"
    }
}


# ============================================================================
# ANGOLA MAPPING
# ============================================================================

ANGOLA_EPR_TO_JP_MAPPING = {
    "Ovimbundu-Ovambo": {
        "keywords": ["ovimbundu", "ovambo", "umbundu", "kwanyama"],
        "match_by_language": "Umbundu"
    },
    "Mbundu-Mestico": {
        "keywords": ["mbundu", "kimbundu"],
        "match_by_language": "Kimbundu"
    },
    "Bakongo": {
        "keywords": ["bakongo", "kongo", "kikongo"],
        "match_by_language": "Koongo"
    },
    "Lunda-Chokwe": {
        "keywords": ["lunda", "chokwe", "cokwe"],
        "match_by_language": "Chokwe"
    },
    "Cabindan Mayombe": {
        "keywords": ["mayombe", "cabinda"]
    }
}


# ============================================================================
# MOZAMBIQUE MAPPING
# ============================================================================

MOZAMBIQUE_EPR_TO_JP_MAPPING = {
    "Tsonga-Chopi": {
        "keywords": ["tsonga", "chopi", "tswa", "shangaan"],
        "match_by_language": "Tsonga"
    },
    "Shona-Ndau": {
        "keywords": ["sena", "ndau", "senji", "shona"],
        "match_by_language": "Ndau"
    },
    "Makonde-Yao": {
        "keywords": ["makonde", "yao", "makhuwa", "lomwe", "chwabo"],
        "match_by_language": "Makhuwa"
    }
}


# ============================================================================
# MALI MAPPING
# ============================================================================

MALI_EPR_TO_JP_MAPPING = {
    "Blacks (Mande, Peul, Voltaic etc.)": {
        "keywords": ["bambara", "bamana", "fulani", "fulbe", "peul", "soninke", 
                    "songhai", "dogon", "senufo", "bobo", "malinke", "maninka",
                    "khasonke", "bomu"],
        "exclude": ["tuareg", "tamasheq", "arab", "moor"],
        "match_by_language": "Bamanankan"
    },
    "Tuareg": {
        "keywords": ["tuareg", "tamasheq"],
        "match_by_language": "Tamasheq"
    },
    "Arabs/Moors": {
        "keywords": ["arab", "moor", "mauritanian"]
    }
}


# ============================================================================
# GUATEMALA MAPPING
# ============================================================================

GUATEMALA_EPR_TO_JP_MAPPING = {
    "Maya": {
        "keywords": ["maya", "kekchi", "kiche", "mam", "cakchiquel", "kanjobal", 
                    "kaqchikel", "q'eqchi'", "q'anjob'al"],
        "exclude": ["ladino", "white", "mestizo"],
        "match_by_language": "Q'eqchi'"
    },
    "Ladinos": {
        "keywords": ["guatemalan", "white", "mestizo", "ladino"],
        "exclude": ["maya", "kekchi", "kiche", "mam", "cakchiquel", "kanjobal"]
    },
    "Xinca": {
        "keywords": ["xinca", "xinka"]
    },
    "Garífuna": {
        "keywords": ["garifuna", "garífuna"]
    }
}


# ============================================================================
# ECUADOR MAPPING
# ============================================================================

ECUADOR_EPR_TO_JP_MAPPING = {
    "Whites/mestizos": {
        "keywords": ["ecuadorian", "mestizo", "white"],
        "exclude": ["quichua", "quichua", "shuar", "achuar", "afro", "indigenous"]
    },
    "Indigenous highland peoples (Kichwa)": {
        "keywords": ["quichua", "kichwa"],
        "match_by_language": "Quichua"
    },
    "Afro-Ecuadorians": {
        "keywords": ["afro", "afro-ecuadorian"]
    },
    "Indigenous lowland peoples (Shuar, Achuar etc.)": {
        "keywords": ["shuar", "achuar", "indigenous"]
    }
}


# ============================================================================
# FRANCE MAPPING
# ============================================================================

FRANCE_EPR_TO_JP_MAPPING = {
    "French": {
        "keywords": ["french", "provencal", "languedocian", "auvergnat", "gascon", "alsatian"],
        "exclude": ["roma", "romani", "basque", "corsican"],
        "match_by_language": "French"
    },
    "Roma": {
        "keywords": ["roma", "romani", "gypsy", "romani, french"],
        "match_by_language": "French"
    },
    "Basques": {
        "keywords": ["basque"],
        "match_by_language": "Basque"
    },
    "Corsicans": {
        "keywords": ["corsican", "corsica"]
    }
}


# ============================================================================
# LIBYA MAPPING
# ============================================================================

LIBYA_EPR_TO_JP_MAPPING = {
    "Arabs": {
        "keywords": ["arab", "libyan", "bedouin", "cyrenaican", "fezzan", "sirtican", "sanusi"],
        "exclude": ["berber", "tuareg", "toubou", "nafusi"],
        "match_by_language": "Arabic"
    },
    "Berbers": {
        "keywords": ["berber", "nafusi", "zuwarah", "jalo", "jabal nafusah"],
        "match_by_language": "Nafusi"
    },
    "Tuareg": {
        "keywords": ["tuareg", "tamasheq"]
    },
    "Toubou": {
        "keywords": ["toubou", "tubu"]
    }
}


# ============================================================================
# SLOVENIA MAPPING
# ============================================================================

SLOVENIA_EPR_TO_JP_MAPPING = {
    "Slovenes": {
        "keywords": ["slovene", "slovenian"],
        "match_by_language": "Slovenian"
    },
    "Serbs": {
        "keywords": ["serb", "serbian"],
        "match_by_language": "Serbian"
    },
    "Croats": {
        "keywords": ["croat", "croatian"],
        "match_by_language": "Croatian"
    },
    "Bosniaks": {
        "keywords": ["bosniak", "bosnian", "muslim"]
    }
}


# ============================================================================
# TURKMENISTAN MAPPING
# ============================================================================

TURKMENISTAN_EPR_TO_JP_MAPPING = {
    "Turkmen": {
        "keywords": ["turkmen", "turkoman"],
        "match_by_language": "Turkmen"
    },
    "Uzbeks": {
        "keywords": ["uzbek"],
        "match_by_language": "Uzbek"
    },
    "Russians": {
        "keywords": ["russian"],
        "match_by_language": "Russian"
    },
    "Kazakhs": {
        "keywords": ["kazakh"],
        "match_by_language": "Kazakh"
    }
}


# ============================================================================
# NEW ZEALAND MAPPING
# ============================================================================

NEW_ZEALAND_EPR_TO_JP_MAPPING = {
    "New Zealanders": {
        "keywords": ["new zealand", "anglo-new zealander", "pakeha", "new zealander"],
        "exclude": ["maori", "asian", "pacific", "cook islands", "niuean", "tokelauan"],
        "match_by_language": "English"
    },
    "Maori": {
        "keywords": ["maori"],
        "match_by_language": "Maori"
    },
    "Asians": {
        "keywords": ["asian", "chinese", "indian"]
    },
    "Pacific Islanders": {
        "keywords": ["pacific", "cook islands", "niuean", "tokelauan", "samoa", "tonga", "pukapuka", "rakahanga"]
    }
}


# ============================================================================
# GREECE MAPPING
# ============================================================================

GREECE_EPR_TO_JP_MAPPING = {
    "Greeks": {
        "keywords": ["greek", "arvanites", "sarakatsani", "tsakonian", "meglenite"],
        "exclude": ["roma", "romani", "macedonian", "muslim", "aromanian"],
        "match_by_language": "Greek"
    },
    "Roma": {
        "keywords": ["roma", "romani", "gypsy", "romani, greek"],
        "match_by_language": "Greek"
    },
    "Macedonians": {
        "keywords": ["macedonian", "slavic"]
    },
    "Muslims": {
        "keywords": ["muslim", "turkish"],
        "exclude": ["greek"]
    }
}


# ============================================================================
# IRAN MAPPING
# ============================================================================

IRAN_EPR_TO_JP_MAPPING = {
    "Persians": {
        "keywords": ["persian", "farsi", "iranian"],
        "exclude": ["azerbaijani", "kurd", "arab", "baloch", "turkmen", "armenian", "assyrian"],
        "match_by_language": "Persian"
    },
    "Azeri": {
        "keywords": ["azerbaijani", "azeri", "turk", "azerbaijan"],
        "match_by_language": "Azerbaijani"
    },
    "Kurds": {
        "keywords": ["kurd", "kurdish"],
        "match_by_language": "Kurdish"
    },
    "Arabs": {
        "keywords": ["arab", "arabic"],
        "exclude": ["persian", "azerbaijani", "kurd"],
        "match_by_language": "Arabic"
    },
    "Baloch": {
        "keywords": ["baloch", "baluch", "baluchi"],
        "match_by_language": "Balochi"
    },
    "Turkmen": {
        "keywords": ["turkmen", "turkoman"],
        "match_by_language": "Turkmen"
    },
    "Armenians": {
        "keywords": ["armenian"],
        "match_by_language": "Armenian"
    },
    "Bahais": {
        "keywords": ["bahai", "baha'i"]
    },
    "Jews": {
        "keywords": ["jewish", "jew"],
        "exclude": ["persian"]
    },
    "Assyrians": {
        "keywords": ["assyrian", "assyro-chaldean"],
        "match_by_language": "Assyrian Neo-Aramaic"
    },
    "Zoroastrians": {
        "keywords": ["zoroastrian", "parsi"]
    }
}


# ============================================================================
# NIGERIA MAPPING
# ============================================================================

NIGERIA_EPR_TO_JP_MAPPING = {
    "Hausa-Fulani and Muslim Middle Belt": {
        "keywords": ["hausa", "fulani", "fulfulde", "kanuri", "muslim"],
        "exclude": ["yoruba", "igbo", "ijaw", "tiv", "ogoni"],
        "match_by_language": "Hausa"
    },
    "Yoruba": {
        "keywords": ["yoruba"],
        "match_by_language": "Yoruba"
    },
    "Igbo": {
        "keywords": ["igbo", "ibo"],
        "match_by_language": "Igbo"
    },
    "Ijaw": {
        "keywords": ["ijaw", "ijo"],
        "match_by_language": "Ijo"
    },
    "Tiv": {
        "keywords": ["tiv"],
        "match_by_language": "Tiv"
    },
    "Ogoni": {
        "keywords": ["ogoni"]
    }
}


# ============================================================================
# ITALY MAPPING
# ============================================================================

ITALY_EPR_TO_JP_MAPPING = {
    "Italians": {
        "keywords": ["italian", "calabrian", "sicilian", "venetian", "lombard", 
                    "emilian", "piedmontese", "ligurian", "tuscan", "neapolitan"],
        "exclude": ["sardinian", "friulian", "german", "french", "roma", "romani"],
        "match_by_language": "Italian"
    },
    "Sardinians": {
        "keywords": ["sardinian", "sardinia"],
        "match_by_language": "Sardinian"
    },
    "Friulians": {
        "keywords": ["friulian", "friuli"],
        "match_by_language": "Friulian"
    },
    "German speakers (Austrians)": {
        "keywords": ["german", "austrian", "tyrolean"],
        "match_by_language": "German"
    },
    "Aostans (French speakers)": {
        "keywords": ["aostan", "french", "valdostan"],
        "match_by_language": "French"
    },
    "Roma": {
        "keywords": ["roma", "romani", "gypsy", "sinti"],
        "match_by_language": "Italian"
    }
}


# ============================================================================
# CANADA MAPPING
# ============================================================================

CANADA_EPR_TO_JP_MAPPING = {
    "English speakers": {
        "keywords": ["anglo-canadian", "canadian", "english", "scottish", "irish", "welsh"],
        "exclude": ["french", "indigenous", "cree", "ojibwa", "inuit"],
        "match_by_language": "English"
    },
    "French speakers": {
        "keywords": ["french-canadian", "french", "quebecois", "acadian"],
        "exclude": ["english", "indigenous"],
        "match_by_language": "French"
    },
    "Indigenous peoples": {
        "keywords": ["indigenous", "cree", "ojibwa", "inuit", "first nations", 
                    "metis", "dene", "haida", "mohawk"],
        "exclude": ["canadian", "english", "french"]
    }
}


# ============================================================================
# EGYPT MAPPING
# ============================================================================

EGYPT_EPR_TO_JP_MAPPING = {
    "Arab Muslims": {
        "keywords": ["arab", "egyptian", "saidi", "bedouin"],
        "exclude": ["coptic", "nubian"],
        "match_by_language": "Arabic"
    },
    "Coptic Christians": {
        "keywords": ["coptic", "egyptian, coptic"],
        "match_by_language": "Arabic"
    }
}


# ============================================================================
# CHINA MAPPING
# ============================================================================

CHINA_EPR_TO_JP_MAPPING = {
    "Chinese (Han)": {
        "keywords": ["han chinese", "chinese", "mandarin", "wu", "cantonese", "jin", "hakka", "min nan", "xiang", "gan"],
        "exclude": ["zhuang", "manchu", "hui", "miao", "uyghur", "tujia", "yi", "mongolian", "tibetan"],
        "match_by_language": "Chinese, Mandarin"
    },
    "Zhuang": {
        "keywords": ["zhuang"],
        "match_by_language": "Zhuang"
    },
    "Manchu": {
        "keywords": ["manchu", "manchurian"],
        "match_by_language": "Manchu"
    },
    "Hui (proper)": {
        "keywords": ["hui", "chinese muslim"],
        "exclude": ["han"]
    },
    "Miao": {
        "keywords": ["miao", "hmong"],
        "match_by_language": "Miao"
    },
    "Uyghur": {
        "keywords": ["uyghur", "uighur"],
        "match_by_language": "Uighur, Uyghur"
    },
    "Tujia": {
        "keywords": ["tujia"],
        "match_by_language": "Tujia"
    },
    "Yi": {
        "keywords": ["yi", "lolo"],
        "match_by_language": "Yi"
    },
    "Mongolians": {
        "keywords": ["mongolian", "mongol"],
        "match_by_language": "Mongolian"
    },
    "Tibetans": {
        "keywords": ["tibetan", "tibet"],
        "match_by_language": "Tibetan"
    },
    "Dong": {
        "keywords": ["dong", "kam"],
        "match_by_language": "Dong, Southern"
    },
    "Bouyei": {
        "keywords": ["bouyei", "buyi"],
        "match_by_language": "Bouyei"
    },
    "Yao": {
        "keywords": ["yao", "mien"],
        "match_by_language": "Mien"
    },
    "Bai": {
        "keywords": ["bai"],
        "match_by_language": "Bai"
    },
    "Koreans": {
        "keywords": ["korean"],
        "match_by_language": "Korean"
    },
    "Hani": {
        "keywords": ["hani"],
        "match_by_language": "Hani"
    },
    "Li": {
        "keywords": ["li", "hainan li"],
        "match_by_language": "Li"
    },
    "Kazakh": {
        "keywords": ["kazakh"],
        "match_by_language": "Kazakh"
    },
    "Dai": {
        "keywords": ["dai", "tai"],
        "match_by_language": "Tai Nua"
    },
    "She": {
        "keywords": ["she"],
        "match_by_language": "She"
    },
    "Lisu": {
        "keywords": ["lisu"],
        "match_by_language": "Lisu"
    },
    "Gelao": {
        "keywords": ["gelao", "gela"],
        "match_by_language": "Gelao"
    },
    "Dongxiang": {
        "keywords": ["dongxiang"],
        "match_by_language": "Dongxiang"
    },
    "Lahu": {
        "keywords": ["lahu"],
        "match_by_language": "Lahu"
    },
    "Shui": {
        "keywords": ["shui"],
        "match_by_language": "Shui"
    },
    "Wa": {
        "keywords": ["wa"],
        "match_by_language": "Wa"
    },
    "Mulam": {
        "keywords": ["mulam", "mulao"],
        "match_by_language": "Mulao"
    },
    "Naxi": {
        "keywords": ["naxi"],
        "match_by_language": "Naxi"
    },
    "Qiang": {
        "keywords": ["qiang"],
        "match_by_language": "Qiang, Northern"
    },
    "Tu": {
        "keywords": ["tu", "monguor"],
        "match_by_language": "Tu"
    },
    "Xibe": {
        "keywords": ["xibe", "sibe"],
        "match_by_language": "Xibe"
    },
    "Kirghiz": {
        "keywords": ["kirghiz", "kyrgyz"],
        "match_by_language": "Kirghiz"
    },
    "Salar": {
        "keywords": ["salar"],
        "match_by_language": "Salar"
    },
    "Daur": {
        "keywords": ["daur", "daghur"],
        "match_by_language": "Daur"
    },
    "Jingpo": {
        "keywords": ["jingpo", "kachin"],
        "match_by_language": "Jingpo"
    },
    "Blang": {
        "keywords": ["blang", "bulang"],
        "match_by_language": "Blang"
    },
    "Maonan": {
        "keywords": ["maonan"],
        "match_by_language": "Maonan"
    }
}


# ============================================================================
# RUSSIA MAPPING
# ============================================================================

RUSSIA_EPR_TO_JP_MAPPING = {
    "Russians": {
        "keywords": ["russian"],
        "exclude": ["tatar", "chechen", "bashkir", "chuvash", "ukrainian"],
        "match_by_language": "Russian"
    },
    "Tatars": {
        "keywords": ["tatar"],
        "match_by_language": "Tatar"
    },
    "Ukrainians": {
        "keywords": ["ukrainian"],
        "match_by_language": "Ukrainian"
    },
    "Chuvashes": {
        "keywords": ["chuvash"],
        "match_by_language": "Chuvash"
    },
    "Bashkirs": {
        "keywords": ["bashkir"],
        "match_by_language": "Bashkort"
    },
    "Chechens": {
        "keywords": ["chechen"],
        "match_by_language": "Chechen"
    },
    "Armenians": {
        "keywords": ["armenian"],
        "match_by_language": "Armenian"
    },
    "Poles": {
        "keywords": ["polish", "pole"],
        "match_by_language": "Polish"
    },
    "Byelorussians": {
        "keywords": ["belarusian", "byelorussian", "belarus"],
        "match_by_language": "Belarusian"
    },
    "Mordva": {
        "keywords": ["mordva", "mordvin"],
        "match_by_language": "Mordvin"
    },
    "Avars": {
        "keywords": ["avar"],
        "match_by_language": "Avar"
    },
    "Kazakhs": {
        "keywords": ["kazakh"],
        "match_by_language": "Kazakh"
    },
    "Azeri": {
        "keywords": ["azerbaijani", "azeri"],
        "match_by_language": "Azerbaijani"
    },
    "Germans": {
        "keywords": ["german"],
        "match_by_language": "German"
    },
    "Dargins": {
        "keywords": ["dargin"],
        "match_by_language": "Dargwa"
    },
    "Ossetes": {
        "keywords": ["ossete", "ossetian"],
        "match_by_language": "Ossetian"
    },
    "Kabardins": {
        "keywords": ["kabardian"],
        "match_by_language": "Kabardian"
    },
    "Mari": {
        "keywords": ["mari"],
        "match_by_language": "Mari"
    },
    "Udmurt": {
        "keywords": ["udmurt"],
        "match_by_language": "Udmurt"
    },
    "Buryats": {
        "keywords": ["buryat", "buriat"],
        "match_by_language": "Buryat"
    },
    "Ingush": {
        "keywords": ["ingush"],
        "match_by_language": "Ingush"
    },
    "Kumyks": {
        "keywords": ["kumyk"],
        "match_by_language": "Kumyk"
    },
    "Lezgins": {
        "keywords": ["lezgin", "lezgi"],
        "match_by_language": "Lezgi"
    },
    "Yakuts": {
        "keywords": ["yakut", "sakha"],
        "match_by_language": "Yakut"
    },
    "Jews": {
        "keywords": ["jewish", "jew"],
        "exclude": ["russian"]
    },
    "Komi": {
        "keywords": ["komi"],
        "match_by_language": "Komi"
    },
    "Koreans": {
        "keywords": ["korean"],
        "match_by_language": "Korean"
    },
    "Tuvinians": {
        "keywords": ["tuvinian", "tuva"],
        "match_by_language": "Tuvinian"
    },
    "Georgians": {
        "keywords": ["georgian"],
        "match_by_language": "Georgian"
    },
    "Adyghe": {
        "keywords": ["adyghe", "adygei"],
        "match_by_language": "Adyghe"
    },
    "Balkars": {
        "keywords": ["balkar"],
        "match_by_language": "Karachay-Balkar"
    },
    "Altai": {
        "keywords": ["altai", "altay"],
        "match_by_language": "Altai, Northern"
    },
    "Roma": {
        "keywords": ["roma", "romani", "gypsy"],
        "match_by_language": "Russian"
    },
    "Kalmyks": {
        "keywords": ["kalmyk"],
        "match_by_language": "Kalmyk-Oirat"
    },
    "Karachai": {
        "keywords": ["karachai", "karachay"],
        "match_by_language": "Karachay-Balkar"
    },
    "Karelians": {
        "keywords": ["karelian"],
        "match_by_language": "Karelian"
    },
    "Khakass": {
        "keywords": ["khakass", "khakas"],
        "match_by_language": "Khakas"
    },
    "Komi-Permyaks": {
        "keywords": ["komi-permyak", "permian"],
        "match_by_language": "Komi-Permyak"
    },
    "Cherkess": {
        "keywords": ["cherkess", "circassian"],
        "match_by_language": "Adyghe"
    },
    "Chukchi": {
        "keywords": ["chukchi", "chukot"],
        "match_by_language": "Chukot"
    }
}


# ============================================================================
# CONGO DRC MAPPING
# ============================================================================

CONGO_DRC_EPR_TO_JP_MAPPING = {
    "Mongo": {
        "keywords": ["mongo", "nkundu"],
        "match_by_language": "Mongo-Nkundu"
    },
    "Bakongo": {
        "keywords": ["kongo", "bakongo", "tuba"],
        "exclude": ["luba", "lingala"],
        "match_by_language": "Kituba"
    },
    "Tetela-Kusu": {
        "keywords": ["tetela", "kusu"],
        "match_by_language": "Tetela"
    },
    "Luba Kasai": {
        "keywords": ["luba", "kasai", "lulua"],
        "exclude": ["katanga", "shaba"],
        "match_by_language": "Luba-Kasai"
    },
    "Lunda-Yeke": {
        "keywords": ["lunda", "yeke"],
        "match_by_language": "Lunda"
    },
    "Luba Shaba": {
        "keywords": ["luba", "shaba", "katanga"],
        "exclude": ["kasai", "lulua"],
        "match_by_language": "Luba-Katanga"
    },
    "Lulua": {
        "keywords": ["lulua"],
        "match_by_language": "Luba-Kasai"
    },
    "Other Kivu groups": {
        "keywords": ["kivu", "hutu", "tutsi", "nyanga", "kumu"]
    },
    "Mbandja": {
        "keywords": ["mbandja", "mbadja"],
        "match_by_language": "Mbandja"
    },
    "Ngbaka": {
        "keywords": ["ngbaka"],
        "match_by_language": "Ngbaka Ma'bo"
    },
    "Ngbandi": {
        "keywords": ["ngbandi"],
        "match_by_language": "Ngbandi"
    },
    "Tutsi-Banyamulenge": {
        "keywords": ["tutsi", "banyamulenge"],
        "match_by_language": "Rundi"
    }
}


# ============================================================================
# CHAD MAPPING
# ============================================================================

CHAD_EPR_TO_JP_MAPPING = {
    "Sara": {
        "keywords": ["sara"],
        "match_by_language": "Sara"
    },
    "Arabs": {
        "keywords": ["arab", "baggara", "shuwa"],
        "exclude": ["sara", "toubou"],
        "match_by_language": "Arabic"
    },
    "Toubou": {
        "keywords": ["toubou", "tubu", "teda"],
        "match_by_language": "Tedaga"
    },
    "Hadjerai": {
        "keywords": ["hadjerai", "hajerai"],
        "match_by_language": "Hajerai"
    },
    "Zaghawa, Bideyat": {
        "keywords": ["zaghawa", "bideyat"],
        "match_by_language": "Zaghawa"
    },
    "Tama": {
        "keywords": ["tama"],
        "match_by_language": "Tama"
    }
}


# ============================================================================
# VIETNAM MAPPING
# ============================================================================

VIETNAM_EPR_TO_JP_MAPPING = {
    "Kinh (Vietnamese)": {
        "keywords": ["vietnamese", "kinh"],
        "exclude": ["hmong", "tay", "thai", "muong", "khmer", "chinese"],
        "match_by_language": "Vietnamese"
    },
    "Tay": {
        "keywords": ["tay"],
        "match_by_language": "Tay"
    },
    "Thai": {
        "keywords": ["thai", "tai dam", "tai don"],
        "exclude": ["vietnamese"],
        "match_by_language": "Tai Dam"
    },
    "Muong": {
        "keywords": ["muong"],
        "match_by_language": "Muong"
    },
    "Khmer": {
        "keywords": ["khmer", "cambodian"],
        "match_by_language": "Khmer"
    },
    "Hoa (Chinese)": {
        "keywords": ["chinese", "hoa"],
        "match_by_language": "Chinese, Mandarin"
    },
    "Hmong": {
        "keywords": ["hmong", "hmong daw"],
        "match_by_language": "Hmong Daw"
    },
    "Nung": {
        "keywords": ["nung"],
        "match_by_language": "Nung"
    },
    "Dao": {
        "keywords": ["dao", "yao"],
        "match_by_language": "Iu Mien"
    },
    "Gia Rai": {
        "keywords": ["jarai", "gia rai"],
        "match_by_language": "Jarai"
    }
}


# ============================================================================
# AUSTRALIA MAPPING
# ============================================================================

AUSTRALIA_EPR_TO_JP_MAPPING = {
    "Whites": {
        "keywords": ["anglo-australian", "australian", "english", "scottish", "irish"],
        "exclude": ["aboriginal", "asian", "torres"],
        "match_by_language": "English"
    },
    "Asians": {
        "keywords": ["asian", "chinese", "indian", "vietnamese"]
    },
    "Aboriginal people": {
        "keywords": ["aboriginal", "torres strait", "pitjantjatjara", "djambarrapuyngu"],
        "exclude": ["anglo", "australian"],
        "match_by_language": "English"
    }
}


# ============================================================================
# BANGLADESH MAPPING
# ============================================================================

BANGLADESH_EPR_TO_JP_MAPPING = {
    "Bengali Muslims": {
        "keywords": ["bengali muslim", "bengali", "sylheti"],
        "exclude": ["hindu", "bihari", "chakma", "rohingya"],
        "match_by_language": "Bengali"
    },
    "Bengali Hindus": {
        "keywords": ["bengali hindu", "namassej"],
        "exclude": ["muslim"],
        "match_by_language": "Bengali"
    },
    "Tribal-Buddhists": {
        "keywords": ["chakma", "marma", "tribal"],
        "match_by_language": "Chakma"
    },
    "Biharis (Urdu-Speaker)": {
        "keywords": ["bihari", "urdu"],
        "match_by_language": "Urdu"
    }
}


# ============================================================================
# BOTSWANA MAPPING
# ============================================================================

BOTSWANA_EPR_TO_JP_MAPPING = {
    "Tswana": {
        "keywords": ["tswana", "setswana", "ngwato", "ngwaketse", "kwena", "tawana"],
        "exclude": ["kalanga", "kgalagadi", "san"],
        "match_by_language": "Setswana"
    },
    "Kalanga": {
        "keywords": ["kalanga"],
        "match_by_language": "Kalanga"
    },
    "Kgalagadi": {
        "keywords": ["kgalagadi", "bangologa"],
        "match_by_language": "Kgalagadi"
    },
    "San": {
        "keywords": ["san", "heikum", "haiom"],
        "match_by_language": "Haiom"
    },
    "Herero/Mbanderu": {
        "keywords": ["herero", "mbanderu"],
        "match_by_language": "Herero"
    },
    "White": {
        "keywords": ["white", "european"]
    },
    "Yeyi": {
        "keywords": ["yeyi"],
        "match_by_language": "Yeyi"
    },
    "Mbukushu": {
        "keywords": ["mbukushu"],
        "match_by_language": "Mbukushu"
    },
    "Birwa": {
        "keywords": ["birwa"],
        "match_by_language": "Birwa"
    },
    "Tswapong": {
        "keywords": ["tswapong"],
        "match_by_language": "Tswapong"
    }
}


# ============================================================================
# VENEZUELA MAPPING
# ============================================================================

VENEZUELA_EPR_TO_JP_MAPPING = {
    "Whites/mestizos": {
        "keywords": ["venezuelan", "mestizo", "white"],
        "exclude": ["warao", "carib", "karina", "pemon", "piaroa"],
        "match_by_language": "Spanish"
    },
    "Afrovenezuelans": {
        "keywords": ["afro", "afro-venezuelan"]
    },
    "Indigenous peoples": {
        "keywords": ["warao", "carib", "karina", "pemon", "piaroa", "paraujano"],
        "match_by_language": "Warao"
    }
}


# ============================================================================
# AZERBAIJAN MAPPING
# ============================================================================

AZERBAIJAN_EPR_TO_JP_MAPPING = {
    "Azeri": {
        "keywords": ["azerbaijani", "azeri"],
        "exclude": ["talysh", "armenian", "avar"],
        "match_by_language": "Azerbaijani"
    },
    "Lezgins": {
        "keywords": ["lezgin", "lezgi"],
        "match_by_language": "Lezgi"
    },
    "Armenians": {
        "keywords": ["armenian"],
        "match_by_language": "Armenian"
    },
    "Talysh": {
        "keywords": ["talysh"],
        "match_by_language": "Talysh"
    }
}


# ============================================================================
# ALGERIA MAPPING
# ============================================================================

ALGERIA_EPR_TO_JP_MAPPING = {
    "Arabs": {
        "keywords": ["algerian", "arab", "arabic-speaking", "bedouin"],
        "exclude": ["berber", "kabyle", "shawiya", "mozabite", "chenoua"],
        "match_by_language": "Arabic"
    },
    "Berbers": {
        "keywords": ["berber", "kabyle", "shawiya", "mozabite", "chenoua", "menasser", "figig"],
        "exclude": ["arab", "algerian, arabic"],
        "match_by_language": "Kabyle"
    }
}


# ============================================================================
# FIJI MAPPING
# ============================================================================

FIJI_EPR_TO_JP_MAPPING = {
    "Fijians": {
        "keywords": ["fijian", "bauan", "rewan", "nadroga", "lauan", "kadavu", "rotuman"],
        "exclude": ["indian", "hindu", "muslim", "hindi"],
        "match_by_language": "Fijian"
    },
    "Indians": {
        "keywords": ["indian", "hindu", "gujarati", "tamil", "fijian hindi"],
        "exclude": ["fijian"],
        "match_by_language": "Hindi"
    }
}


# ============================================================================
# LIBERIA MAPPING
# ============================================================================

LIBERIA_EPR_TO_JP_MAPPING = {
    "Gio": {
        "keywords": ["gio", "dan"],
        "match_by_language": "Dan"
    },
    "Mano": {
        "keywords": ["mano", "maan"],
        "match_by_language": "Maan"
    },
    "Kru": {
        "keywords": ["kru", "klao"],
        "match_by_language": "Klao"
    },
    "Krahn (Guere)": {
        "keywords": ["krahn", "guere"],
        "match_by_language": "Krahn"
    },
    "Americo-Liberians": {
        "keywords": ["americo-liberian", "liberian english"],
        "match_by_language": "English"
    },
    "Mandingo": {
        "keywords": ["mandingo", "mandinka"]
    }
}


# ============================================================================
# ERITREA MAPPING
# ============================================================================

ERITREA_EPR_TO_JP_MAPPING = {
    "Christians": {
        "keywords": ["tigre", "tigrinya", "bilen", "kunama", "nara"],
        "exclude": ["afar", "saho", "muslim"],
        "match_by_language": "Tigre"
    },
    "Other Muslims": {
        "keywords": ["muslim", "afar", "saho"],
        "exclude": ["tigre", "tigrinya", "bilen", "kunama"],
        "match_by_language": "Tigre"
    },
    "Afar": {
        "keywords": ["afar"],
        "match_by_language": "Afar"
    },
    "Saho": {
        "keywords": ["saho", "irob"],
        "match_by_language": "Saho"
    },
    "Kunama": {
        "keywords": ["kunama"],
        "match_by_language": "Kunama"
    }
}


# ============================================================================
# BULGARIA MAPPING
# ============================================================================

BULGARIA_EPR_TO_JP_MAPPING = {
    "Bulgarians": {
        "keywords": ["bulgarian", "bulgar"],
        "exclude": ["turkish", "roma", "romani", "pomak", "macedonian"],
        "match_by_language": "Bulgarian"
    },
    "Turkish": {
        "keywords": ["turkish", "turk"],
        "match_by_language": "Turkish"
    },
    "Roma": {
        "keywords": ["roma", "romani", "gypsy"],
        "match_by_language": "Bulgarian"
    },
    "Pomaks": {
        "keywords": ["pomak"]
    },
    "Macedonians": {
        "keywords": ["macedonian"]
    }
}


# ============================================================================
# SAUDI ARABIA MAPPING
# ============================================================================

SAUDI_ARABIA_EPR_TO_JP_MAPPING = {
    "Sunni Wahhabi (Najdi) (Arab)": {
        "keywords": ["najdi", "saudi", "wahhabi"],
        "exclude": ["hijazi", "shia", "south asian", "urdu"],
        "match_by_language": "Arabic, Najdi"
    },
    "Sunni Shafii/Sofi (Hijazi) (Arab)": {
        "keywords": ["hijazi", "saudi"],
        "exclude": ["najdi", "shia", "south asian"],
        "match_by_language": "Arabic, Hijazi"
    },
    "Ja'afari Shia (Eastern Province) (Arab)": {
        "keywords": ["shia", "ja'afari"]
    },
    "Ismaili Shia (South) (Arab)": {
        "keywords": ["ismaili", "shia"]
    }
}


# ============================================================================
# SYRIA MAPPING
# ============================================================================

SYRIA_EPR_TO_JP_MAPPING = {
    "Sunni Arabs": {
        "keywords": ["arab", "syrian"],
        "exclude": ["alawite", "druze", "assyrian", "aramaic", "kurd"],
        "match_by_language": "Arabic, Levantine"
    },
    "Alawi": {
        "keywords": ["alawite", "alawi"],
        "match_by_language": "Arabic, Levantine"
    },
    "Christians": {
        "keywords": ["assyrian", "aramaic", "christian"],
        "exclude": ["arab", "alawite"],
        "match_by_language": "Assyrian Neo-Aramaic"
    },
    "Kurds": {
        "keywords": ["kurd", "kurdish"]
    },
    "Druze": {
        "keywords": ["druze"],
        "match_by_language": "Arabic, Levantine"
    }
}


# ============================================================================
# FINLAND MAPPING
# ============================================================================

FINLAND_EPR_TO_JP_MAPPING = {
    "Finns": {
        "keywords": ["finnish", "finland"],
        "exclude": ["swede", "swedish", "saami", "romani"],
        "match_by_language": "Finnish"
    },
    "Swedes": {
        "keywords": ["swede", "swedish", "finland swede"],
        "match_by_language": "Swedish"
    }
}


# ============================================================================
# CUBA MAPPING
# ============================================================================

CUBA_EPR_TO_JP_MAPPING = {
    "Whites": {
        "keywords": ["cuban"],
        "exclude": ["mulatto", "black"],
        "match_by_language": "Spanish"
    },
    "Afro-Cubans": {
        "keywords": ["mulatto", "black", "afro"],
        "match_by_language": "Spanish"
    }
}


# ============================================================================
# CAPE VERDE MAPPING
# ============================================================================

CAPE_VERDE_EPR_TO_JP_MAPPING = {
    "Creoles": {
        "keywords": ["cape verdean", "creole", "crioulo"],
        "match_by_language": "Crioulo, Upper Guinea"
    }
}


# ============================================================================
# JAMAICA MAPPING
# ============================================================================

JAMAICA_EPR_TO_JP_MAPPING = {
    "Blacks": {
        "keywords": ["jamaican", "afro-jamaican", "black"],
        "exclude": ["chinese", "indian", "white"],
        "match_by_language": "English"
    }
}


# ============================================================================
# SUDAN MAPPING
# ============================================================================

SUDAN_EPR_TO_JP_MAPPING = {
    "Shaygiyya, Ja'aliyyin and Danagla (Arab)": {
        "keywords": ["arab", "shaygiyya", "ja'aliyyin", "danagla"],
        "exclude": ["dinka", "nuer", "nuba", "beja", "azande", "bari"],
        "match_by_language": "Arabic"
    },
    "Dinka": {
        "keywords": ["dinka"],
        "match_by_language": "Dinka"
    },
    "Nuer": {
        "keywords": ["nuer"],
        "match_by_language": "Nuer"
    },
    "Beja": {
        "keywords": ["beja"],
        "match_by_language": "Beja"
    },
    "Nuba": {
        "keywords": ["nuba"]
    },
    "Azande": {
        "keywords": ["azande", "zande"],
        "match_by_language": "Zande"
    },
    "Bari": {
        "keywords": ["bari"]
    },
    "Other Arab Groups": {
        "keywords": ["arab"],
        "exclude": ["dinka", "nuer", "nuba", "beja", "azande", "bari"],
        "match_by_language": "Arabic"
    },
    "Other Northern Groups": {
        "keywords": ["northern"]
    },
    "Other Southern groups": {
        "keywords": ["southern"]
    }
}


# ============================================================================
# ISRAEL MAPPING
# ============================================================================

ISRAEL_EPR_TO_JP_MAPPING = {
    "Ashkenazim (Jewish)": {
        "keywords": ["ashkenazi", "jewish", "israeli"],
        "exclude": ["mizrahi", "palestinian", "arab", "russian"],
        "match_by_language": "Hebrew"
    },
    "Mizrahim (Jewish)": {
        "keywords": ["mizrahi", "jewish", "israeli"],
        "exclude": ["ashkenazi", "palestinian", "arab"],
        "match_by_language": "Hebrew"
    },
    "Russians (Jewish)": {
        "keywords": ["russian", "jewish"],
        "exclude": ["palestinian", "arab"],
        "match_by_language": "Russian"
    },
    "Palestinian Arabs": {
        "keywords": ["palestinian", "arab"],
        "exclude": ["jewish", "israeli"],
        "match_by_language": "Arabic"
    },
    "Israeli Arabs": {
        "keywords": ["arab", "israeli"],
        "exclude": ["jewish", "palestinian"],
        "match_by_language": "Arabic"
    }
}


# ============================================================================
# JAPAN MAPPING
# ============================================================================

JAPAN_EPR_TO_JP_MAPPING = {
    "Japanese": {
        "keywords": ["japanese"],
        "exclude": ["okinawan", "korean", "ainu", "burakumin"],
        "match_by_language": "Japanese"
    },
    "Okinawans": {
        "keywords": ["okinawan", "ryukyuan"],
        "match_by_language": "Okinawan, Central"
    },
    "Koreans": {
        "keywords": ["korean"],
        "match_by_language": "Korean"
    },
    "Burakumin": {
        "keywords": ["burakumin"]
    },
    "Ainu": {
        "keywords": ["ainu"]
    }
}


# ============================================================================
# SPAIN MAPPING
# ============================================================================

SPAIN_EPR_TO_JP_MAPPING = {
    "Spanish": {
        "keywords": ["spanish", "spain"],
        "exclude": ["catalan", "galician", "basque", "roma", "romani"],
        "match_by_language": "Spanish"
    },
    "Catalans": {
        "keywords": ["catalan", "catalonia"],
        "match_by_language": "Catalan"
    },
    "Galicians": {
        "keywords": ["galician", "galicia"],
        "match_by_language": "Galician"
    },
    "Basques": {
        "keywords": ["basque", "euskara"],
        "match_by_language": "Basque"
    },
    "Roma": {
        "keywords": ["roma", "romani", "gypsy"],
        "match_by_language": "Spanish"
    }
}


# ============================================================================
# MOROCCO MAPPING
# ============================================================================

MOROCCO_EPR_TO_JP_MAPPING = {
    "Arabs": {
        "keywords": ["arab", "moroccan"],
        "exclude": ["berber", "sahrawi"],
        "match_by_language": "Arabic, Moroccan"
    },
    "Berbers": {
        "keywords": ["berber", "amazigh", "tamazight"],
        "exclude": ["arab"],
        "match_by_language": "Tamazight, Central Atlas"
    },
    "Sahrawis": {
        "keywords": ["sahrawi", "sahraoui"]
    }
}


# ============================================================================
# TOGO MAPPING
# ============================================================================

TOGO_EPR_TO_JP_MAPPING = {
    "Ewe (and related groups)": {
        "keywords": ["ewe"],
        "exclude": ["kabre", "kabiyé"],
        "match_by_language": "Ewe"
    },
    "Kabré (and related groups)": {
        "keywords": ["kabre", "kabiyé", "kabye"],
        "match_by_language": "Kabye"
    }
}


# ============================================================================
# TURKEY MAPPING
# ============================================================================

TURKEY_EPR_TO_JP_MAPPING = {
    "Turkish": {
        "keywords": ["turkish", "turk"],
        "exclude": ["kurd", "roma", "romani"],
        "match_by_language": "Turkish"
    },
    "Kurds": {
        "keywords": ["kurd", "kurdish"],
        "match_by_language": "Kurdish, Northern"
    },
    "Roma": {
        "keywords": ["roma", "romani", "gypsy"],
        "match_by_language": "Turkish"
    }
}


# ============================================================================
# ZIMBABWE MAPPING
# ============================================================================

ZIMBABWE_EPR_TO_JP_MAPPING = {
    "Shona": {
        "keywords": ["shona"],
        "exclude": ["ndebele", "kalanga", "tonga", "white"],
        "match_by_language": "Shona"
    },
    "Ndebele-Kalanga-(Tonga)": {
        "keywords": ["ndebele", "kalanga", "tonga"],
        "exclude": ["shona", "white"],
        "match_by_language": "Ndebele"
    },
    "White Zimbabweans": {
        "keywords": ["white", "zimbabwean"]
    }
}


# ============================================================================
# PARAGUAY MAPPING
# ============================================================================

PARAGUAY_EPR_TO_JP_MAPPING = {
    "Whites/mestizos": {
        "keywords": ["paraguayan", "mestizo", "white"],
        "exclude": ["guarani", "indigenous", "tupi"],
        "match_by_language": "Spanish"
    },
    "Tupi-Guaraní and other indigenous groups": {
        "keywords": ["guarani", "tupi", "indigenous"],
        "match_by_language": "Guarani, Paraguayan"
    }
}


# ============================================================================
# POLAND MAPPING
# ============================================================================

POLAND_EPR_TO_JP_MAPPING = {
    "Poles": {
        "keywords": ["polish", "pole"],
        "exclude": ["ukrainian", "german", "belarusian", "roma", "romani", "jewish"],
        "match_by_language": "Polish"
    },
    "Ukrainians": {
        "keywords": ["ukrainian"],
        "match_by_language": "Ukrainian"
    },
    "Germans": {
        "keywords": ["german"],
        "match_by_language": "German"
    },
    "Byelorussians": {
        "keywords": ["belarusian", "byelorussian"],
        "match_by_language": "Belarusian"
    },
    "Roma": {
        "keywords": ["roma", "romani", "gypsy"],
        "match_by_language": "Romani, Baltic"
    },
    "European and American Jews": {
        "keywords": ["jewish", "jew"]
    }
}


# ============================================================================
# CROATIA MAPPING
# ============================================================================

CROATIA_EPR_TO_JP_MAPPING = {
    "Croats": {
        "keywords": ["croat", "croatian"],
        "exclude": ["serb", "bosniak", "italian", "roma", "hungarian"],
        "match_by_language": "Croatian"
    },
    "Serbs": {
        "keywords": ["serb", "serbian"],
        "match_by_language": "Serbian"
    },
    "Bosniaks": {
        "keywords": ["bosniak", "bosnian"]
    },
    "Italians": {
        "keywords": ["italian"]
    },
    "Roma": {
        "keywords": ["roma", "romani"]
    },
    "Hungarians": {
        "keywords": ["hungarian"]
    }
}


# ============================================================================
# HONDURAS MAPPING
# ============================================================================

HONDURAS_EPR_TO_JP_MAPPING = {
    "Whites/mestizos": {
        "keywords": ["honduran", "mestizo", "white"],
        "exclude": ["lenca", "maya", "miskito", "garifuna", "indigenous"],
        "match_by_language": "Spanish"
    },
    "Indigenous peoples (Lenca, Maya-Chorti, Miskito, Tawahka/Sumu, Xicaque, Pech, Nahua)": {
        "keywords": ["lenca", "maya", "miskito", "tawahka", "sumu", "xicaque", "pech", "nahua", "indigenous"],
        "match_by_language": "Spanish"
    },
    "Garifuna": {
        "keywords": ["garifuna"],
        "match_by_language": "Garifuna"
    }
}


# ============================================================================
# UZBEKISTAN MAPPING
# ============================================================================

UZBEKISTAN_EPR_TO_JP_MAPPING = {
    "Uzbeks": {
        "keywords": ["uzbek"],
        "exclude": ["russian", "tajik", "karakalpak"],
        "match_by_language": "Uzbek, Northern"
    },
    "Russians": {
        "keywords": ["russian"],
        "match_by_language": "Russian"
    },
    "Tajiks": {
        "keywords": ["tajik"],
        "match_by_language": "Tajik"
    },
    "Karakalpak": {
        "keywords": ["karakalpak"],
        "match_by_language": "Karakalpak"
    }
}


# ============================================================================
# PORTUGAL MAPPING
# ============================================================================

PORTUGAL_EPR_TO_JP_MAPPING = {
    "Portuguese": {
        "keywords": ["portuguese", "portugal"],
        "match_by_language": "Portuguese"
    }
}


# ============================================================================
# SOMALIA MAPPING
# ============================================================================

SOMALIA_EPR_TO_JP_MAPPING = {
    "Somali": {
        "keywords": ["somali"],
        "match_by_language": "Somali"
    }
}


# ============================================================================
# SWEDEN MAPPING
# ============================================================================

SWEDEN_EPR_TO_JP_MAPPING = {
    "Swedes": {
        "keywords": ["swedish", "swede"],
        "match_by_language": "Swedish"
    }
}


# ============================================================================
# CYPRUS MAPPING
# ============================================================================

CYPRUS_EPR_TO_JP_MAPPING = {
    "Greeks": {
        "keywords": ["greek", "cypriot"],
        "exclude": ["turkish", "turk"],
        "match_by_language": "Greek"
    },
    "Turks": {
        "keywords": ["turkish", "turk", "cypriot"],
        "exclude": ["greek"],
        "match_by_language": "Turkish"
    }
}


# ============================================================================
# HUNGARY MAPPING
# ============================================================================

HUNGARY_EPR_TO_JP_MAPPING = {
    "Hungarians": {
        "keywords": ["hungarian"],
        "exclude": ["roma", "romani"],
        "match_by_language": "Hungarian"
    },
    "Roma": {
        "keywords": ["roma", "romani"],
        "match_by_language": "Hungarian"
    }
}


# ============================================================================
# NETHERLANDS MAPPING
# ============================================================================

NETHERLANDS_EPR_TO_JP_MAPPING = {
    "Dutch": {
        "keywords": ["dutch", "netherlands"],
        "match_by_language": "Dutch"
    }
}


# ============================================================================
# NORWAY MAPPING
# ============================================================================

NORWAY_EPR_TO_JP_MAPPING = {
    "Norwegians": {
        "keywords": ["norwegian", "norway"],
        "match_by_language": "Norwegian"
    }
}


# ============================================================================
# DOMINICAN REPUBLIC MAPPING
# ============================================================================

DOMINICAN_REPUBLIC_EPR_TO_JP_MAPPING = {
    "Dominicans": {
        "keywords": ["dominican"],
        "match_by_language": "Spanish"
    }
}


# ============================================================================
# UNITED ARAB EMIRATES MAPPING
# ============================================================================

UNITED_ARAB_EMIRATES_EPR_TO_JP_MAPPING = {
    "Emirati Arabs": {
        "keywords": ["emirati", "arab", "uae", "gulf"],
        "exclude": ["south asian", "telugu", "sinhalese"],
        "match_by_language": "Arabic"
    }
}


# ============================================================================
# DENMARK MAPPING
# ============================================================================

DENMARK_EPR_TO_JP_MAPPING = {
    "Danes": {
        "keywords": ["danish", "denmark", "dane"],
        "match_by_language": "Danish"
    }
}


# ============================================================================
# GENERIC MAPPING FUNCTION
# ============================================================================

def build_country_epr_to_jp_mapping(jp_groups: list, country_mapping: dict) -> dict:
    """
    Build EPR → JP mapping for a country.
    
    Args:
        jp_groups: List of all JP groups for the country
        country_mapping: Country-specific mapping dict
    
    Returns:
        Dict mapping EPR group name → list of JP group dicts
    """
    epr_groups = list(country_mapping.keys())
    mapping = {}
    
    for epr_group in epr_groups:
        matching_jp = get_jp_groups_for_epr_generic(epr_group, jp_groups, country_mapping)
        mapping[epr_group] = matching_jp
    
    return mapping


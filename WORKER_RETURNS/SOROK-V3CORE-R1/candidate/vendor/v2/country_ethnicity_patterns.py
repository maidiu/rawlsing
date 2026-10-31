def _apply_country_specific_patterns(country_name: str, ethnicity: str) -> str:
    """
    Apply country-specific pattern matching for ethnicity names.
    
    Returns mapped name if pattern matches, otherwise returns original ethnicity.
    """
    ethnicity_lower = ethnicity.lower()
    
    # Indonesia patterns
    if country_name == "Indonesia":
        if ethnicity.startswith("Java ") or (ethnicity != "Javanese" and "Java" in ethnicity):
            return "Javanese"
        elif ethnicity.startswith("Batak"):
            return "Bataks"
        elif ethnicity.startswith("Malay"):
            return "Malay"
        elif "Bugis" in ethnicity or "Makassar" in ethnicity or "Makasar" in ethnicity:
            return "Makassarese and Bugis"
        elif "Papuan" in ethnicity or ("Papua" in ethnicity and "Papuan" not in ethnicity):
            return "Papuans"
    
    # China patterns
    elif country_name == "China":
        # Minority groups first (before Han pattern)
        # Hui (proper)
        if "hui" in ethnicity_lower and "han" not in ethnicity_lower:
            return "Hui (proper)"
        # Uyghur
        elif "uyghur" in ethnicity_lower or "uighur" in ethnicity_lower:
            return "Uyghur"
        # Tujia
        elif "tujia" in ethnicity_lower:
            return "Tujia"
        # Bouyei
        elif "bouyei" in ethnicity_lower:
            return "Bouyei"
        # Tibetans
        elif "tibetan" in ethnicity_lower or "tibet" in ethnicity_lower:
            return "Tibetans"
        # Mongolians
        elif "mongolian" in ethnicity_lower or "mongol" in ethnicity_lower:
            return "Mongolians"
        # Exact matches for other minority groups
        elif ethnicity_lower in ["zhuang", "manchu", "miao", "yi", "dong", "yao", "bai", 
                                 "koreans", "hani", "li", "kazakh", "dai", "she", "lisu", 
                                 "gelao", "dongxiang", "lahu", "shui", "wa", "mulam", "naxi", 
                                 "qiang", "tu", "xibe", "kirghiz", "salar", "daur", "jingpo", 
                                 "blang", "maonan"]:
            return ethnicity.title()  # Capitalize first letter
        # Han pattern (most common - 91.5% of population)
        # All "Han Chinese, *" variants map to "Chinese (Han)"
        elif "han" in ethnicity_lower or "chinese" in ethnicity_lower:
            return "Chinese (Han)"
        # Subgroups: Check if contains main group name
        elif "zhuang" in ethnicity_lower:
            return "Zhuang"
        elif "manchu" in ethnicity_lower:
            return "Manchu"
        elif "hui" in ethnicity_lower and "hui" not in ["hui proper", "hui (proper)"]:
            return "Hui (proper)"
        elif "miao" in ethnicity_lower:
            return "Miao"
        elif "uyghur" in ethnicity_lower or "uighur" in ethnicity_lower:
            return "Uyghur"
        elif "tujia" in ethnicity_lower:
            return "Tujia"
        elif "yi" in ethnicity_lower and ethnicity_lower not in ["yi", "yiyi"]:
            return "Yi"
        elif "mongolian" in ethnicity_lower or "mongol" in ethnicity_lower:
            return "Mongolians"
        elif "tibetan" in ethnicity_lower or "tibet" in ethnicity_lower:
            return "Tibetans"
        elif "dong" in ethnicity_lower:
            return "Dong"
        elif "bouyei" in ethnicity_lower:
            return "Bouyei"
        elif "yao" in ethnicity_lower:
            return "Yao"
        elif "bai" in ethnicity_lower:
            return "Bai"
        elif "korean" in ethnicity_lower:
            return "Koreans"
        elif "hani" in ethnicity_lower:
            return "Hani"
        elif "li" in ethnicity_lower and ethnicity_lower not in ["li", "lili"]:
            return "Li"
        elif "kazakh" in ethnicity_lower:
            return "Kazakh"
        elif "dai" in ethnicity_lower:
            return "Dai"
        elif "she" in ethnicity_lower and ethnicity_lower not in ["she", "sheshe"]:
            return "She"
        elif "lisu" in ethnicity_lower:
            return "Lisu"
        elif "gelao" in ethnicity_lower:
            return "Gelao"
        elif "dongxiang" in ethnicity_lower:
            return "Dongxiang"
        elif "lahu" in ethnicity_lower:
            return "Lahu"
        elif "shui" in ethnicity_lower:
            return "Shui"
        elif "wa" in ethnicity_lower and ethnicity_lower not in ["wa", "wawa"]:
            return "Wa"
        elif "mulam" in ethnicity_lower:
            return "Mulam"
        elif "naxi" in ethnicity_lower:
            return "Naxi"
        elif "qiang" in ethnicity_lower:
            return "Qiang"
        elif "tu" in ethnicity_lower and ethnicity_lower not in ["tu", "tutu"]:
            return "Tu"
        elif "xibe" in ethnicity_lower:
            return "Xibe"
        elif "kirghiz" in ethnicity_lower or "kyrgyz" in ethnicity_lower:
            return "Kirghiz"
        elif "salar" in ethnicity_lower:
            return "Salar"
        elif "daur" in ethnicity_lower:
            return "Daur"
        elif "jingpo" in ethnicity_lower:
            return "Jingpo"
        elif "blang" in ethnicity_lower:
            return "Blang"
        elif "maonan" in ethnicity_lower:
            return "Maonan"
    
    # India patterns
    elif country_name == "India":
        # Caste/community-based patterns (most JP groups are specific castes/communities)
        # These map to EPR language groups or caste categories
        
        # Scheduled Castes (SC/Dalit)
        if any(term in ethnicity_lower for term in ["scheduled caste", "sc", "dalit", "harijan", 
                                                     "chamar", "pasi", "dusadh", "khatik", "valmiki"]):
            return "Scheduled Castes"
        
        # Scheduled Tribes (ST/Adivasi)
        elif any(term in ethnicity_lower for term in ["scheduled tribe", "st", "adivasi", "tribal", 
                                                       "gond", "santal", "bhil", "munda", "oraon"]):
            return "Scheduled Tribes"
        
        # OBC (Other Backward Classes) - many castes fall here
        elif any(term in ethnicity_lower for term in ["obc", "other backward", "yadav", "kurmi", 
                                                      "gupta", "patel", "jain", "vaishya"]):
            return "Other Backward Classes/Castes"
        
        # Muslims (most common Muslim communities)
        elif any(term in ethnicity_lower for term in ["muslim", "shaikh", "syed", "pathan", "ansari", 
                                                     "khan", "sheikh", "momin"]):
            if "kashmiri" in ethnicity_lower:
                return "Kashmiri Muslims"
            else:
                return "Other Muslims"
        
        # Sikhs
        elif any(term in ethnicity_lower for term in ["sikh", "punjabi", "jat sikh"]):
            return "Punjabi-Sikhs (non-SC/ST/OBCs)"
        
        # Language-based patterns (when language is explicit)
        elif "hindi" in ethnicity_lower:
            return "Hindi (Non SC/ST OBCs)"
        elif "bengali" in ethnicity_lower:
            return "Bengali (non-SC/ST/OBCs)"
        elif "tamil" in ethnicity_lower:
            return "Tamil (non-SC/ST/OBCs)"
        elif "telugu" in ethnicity_lower:
            return "Telugu (Non SC/ST/OBCs)"
        elif "marathi" in ethnicity_lower:
            return "Marathi (non-SC/ST)"
        elif "gujarati" in ethnicity_lower:
            return "Gujarati (non-SC/ST)"
        elif "kannada" in ethnicity_lower:
            return "Kannada (non-SC/ST)"
        elif "malayalam" in ethnicity_lower or "malyalam" in ethnicity_lower:
            return "Malyalam (non-SC/ST)"
        elif "oriya" in ethnicity_lower or "odia" in ethnicity_lower:
            return "Oriya (non-SC/ST)"
        elif "assamese" in ethnicity_lower:
            return "Assamese (non-SC/ST/OBCs)"
        
        # Regional/ethnic patterns
        elif "manipuri" in ethnicity_lower or "meitei" in ethnicity_lower:
            return "Manipuri"
        elif "naga" in ethnicity_lower:
            return "Naga"
        elif "bodo" in ethnicity_lower:
            return "Bodo"
        elif "mizo" in ethnicity_lower:
            return "Mizo"
        elif "tripuri" in ethnicity_lower:
            return "Indigenous Tripuri"
        
        # Default: Most upper-caste Hindu groups map to Hindi (largest group)
        # This is a fallback for groups that don't match above patterns
        elif any(term in ethnicity_lower for term in ["brahmin", "rajput", "thakur", "kayastha", 
                                                       "baniya", "vaishya", "kshatriya"]):
            return "Hindi (Non SC/ST OBCs)"
    
    # Top 20 countries patterns (auto-generated)
    elif country_name == "Russia (Soviet Union)":
        if "russian" in ethnicity_lower:
            return "Russians"
        elif "tatar" in ethnicity_lower:
            return "Tatars"
        elif "ukrainian" in ethnicity_lower:
            return "Ukrainians"
        elif "chechen" in ethnicity_lower:
            return "Chechens"
        elif "bashkir" in ethnicity_lower:
            return "Bashkirs"
        elif "chuvash" in ethnicity_lower:
            return "Chuvash"
        elif "armenian" in ethnicity_lower:
            return "Armenians"
        elif "avars" in ethnicity_lower or "avar" in ethnicity_lower:
            return "Avars"
        elif "azeri" in ethnicity_lower or "azerbaijani" in ethnicity_lower:
            return "Azeri"
        elif "kabardian" in ethnicity_lower:
            return "Kabardians"
        elif "dargin" in ethnicity_lower:
            return "Dargins"
        elif "kumyk" in ethnicity_lower:
            return "Kumyks"
        elif "lezgin" in ethnicity_lower:
            return "Lezgins"
        elif "mordvin" in ethnicity_lower:
            return "Mordvins"
        elif "udmurt" in ethnicity_lower:
            return "Udmurts"
        elif "mari" in ethnicity_lower:
            return "Mari"
        elif "ossetian" in ethnicity_lower or "osset" in ethnicity_lower:
            return "Ossetians"
        elif "yakuts" in ethnicity_lower or "yakut" in ethnicity_lower:
            return "Yakuts"
        elif "buryat" in ethnicity_lower:
            return "Buryats"
        elif "tuvinian" in ethnicity_lower or "tuva" in ethnicity_lower:
            return "Tuvinians"
        elif "kalmyk" in ethnicity_lower:
            return "Kalmyks"
        elif "ingush" in ethnicity_lower:
            return "Ingush"
        elif "karelian" in ethnicity_lower:
            return "Karelians"
        elif "komi" in ethnicity_lower:
            return "Komi"
        elif "altai" in ethnicity_lower:
            return "Altai"
        elif "khakas" in ethnicity_lower:
            return "Khakas"
        elif "adyghe" in ethnicity_lower or "adygei" in ethnicity_lower:
            return "Adyghe"
        elif "balkar" in ethnicity_lower:
            return "Balkars"
        elif "karachay" in ethnicity_lower:
            return "Karachay"
        elif "noghay" in ethnicity_lower or "nogai" in ethnicity_lower:
            return "Noghay"
        elif "turkmen" in ethnicity_lower:
            return "Turkmen"
        elif "uzbek" in ethnicity_lower:
            return "Uzbeks"
        elif "kazakh" in ethnicity_lower:
            return "Kazakhs"
        elif "kirghiz" in ethnicity_lower or "kyrgyz" in ethnicity_lower:
            return "Kirghiz"
        elif "tajik" in ethnicity_lower:
            return "Tajiks"
        elif "jewish" in ethnicity_lower or "jew" in ethnicity_lower:
            return "Jews"
    
    elif country_name == "Sudan":
        if "arab" in ethnicity_lower:
            return "Arabs"
        elif "nubian" in ethnicity_lower:
            return "Nubians"
        elif "beja" in ethnicity_lower:
            return "Beja"
        elif "fur" in ethnicity_lower:
            return "Fur"
        elif "nuba" in ethnicity_lower:
            return "Nuba"
        elif "zaghawa" in ethnicity_lower:
            return "Zaghawa"
        elif "masalit" in ethnicity_lower:
            return "Masalit"
        elif "dinka" in ethnicity_lower:
            return "Dinka"
        elif "nuer" in ethnicity_lower:
            return "Nuer"
        elif "shilluk" in ethnicity_lower:
            return "Shilluk"
        elif "anyuak" in ethnicity_lower:
            return "Anyuak"
        elif "bari" in ethnicity_lower:
            return "Bari"
        elif "azande" in ethnicity_lower:
            return "Azande"
        elif "fertit" in ethnicity_lower:
            return "Fertit"
        elif "murle" in ethnicity_lower:
            return "Murle"
    
    elif country_name == "South Africa":
        if "zulu" in ethnicity_lower:
            return "Zulu"
        elif "xhosa" in ethnicity_lower:
            return "Xhosa"
        elif "afrikaner" in ethnicity_lower or "afrikaans" in ethnicity_lower:
            return "Afrikaners"
        elif "coloured" in ethnicity_lower:
            return "Coloureds"
        elif "sotho" in ethnicity_lower or "sesotho" in ethnicity_lower:
            return "Sotho"
        elif "tswana" in ethnicity_lower:
            return "Tswana"
        elif "tsonga" in ethnicity_lower:
            return "Tsonga"
        elif "swazi" in ethnicity_lower:
            return "Swazi"
        elif "venda" in ethnicity_lower:
            return "Venda"
        elif "ndebele" in ethnicity_lower:
            return "Ndebele"
        elif "english" in ethnicity_lower and "speaking" in ethnicity_lower:
            return "English-speakers"
        elif "indian" in ethnicity_lower and "south africa" in ethnicity_lower:
            return "Indians"
    
    elif country_name == "Myanmar (Burma)":
        if "burman" in ethnicity_lower or "bamar" in ethnicity_lower:
            return "Burmans"
        elif "shan" in ethnicity_lower:
            return "Shan"
        elif "karen" in ethnicity_lower:
            return "Karen"
        elif "rakhine" in ethnicity_lower or "arakanese" in ethnicity_lower:
            return "Rakhine"
        elif "mon" in ethnicity_lower and "mongolian" not in ethnicity_lower:
            return "Mon"
        elif "chin" in ethnicity_lower:
            return "Chin"
        elif "kachin" in ethnicity_lower:
            return "Kachin"
        elif "kayah" in ethnicity_lower:
            return "Kayah"
        elif "kayin" in ethnicity_lower:
            return "Kayin"
        elif "wa" in ethnicity_lower and "wawa" not in ethnicity_lower:
            return "Wa"
        elif "palaung" in ethnicity_lower:
            return "Palaung"
    
    elif country_name == "Congo, Democratic Republic of (Zaire)":
        if "luba" in ethnicity_lower:
            return "Luba"
        elif "kongo" in ethnicity_lower:
            return "Kongo"
        elif "mong" in ethnicity_lower or "mongo" in ethnicity_lower:
            return "Mongo"
        elif "runda" in ethnicity_lower:
            return "Runda"
        elif "lunda" in ethnicity_lower:
            return "Lunda"
        elif "tetela" in ethnicity_lower:
            return "Tetela"
        elif "chokwe" in ethnicity_lower:
            return "Chokwe"
        elif "ngbandi" in ethnicity_lower:
            return "Ngbandi"
        elif "zande" in ethnicity_lower or "azande" in ethnicity_lower:
            return "Zande"
        elif "hutu" in ethnicity_lower:
            return "Hutu"
        elif "tutsi" in ethnicity_lower:
            return "Tutsi"
        elif "pygmy" in ethnicity_lower:
            return "Pygmies"
    
    elif country_name == "Namibia":
        if "ovambo" in ethnicity_lower:
            return "Ovambo"
        elif "kavango" in ethnicity_lower:
            return "Kavango"
        elif "herero" in ethnicity_lower:
            return "Herero"
        elif "damara" in ethnicity_lower:
            return "Damara"
        elif "nama" in ethnicity_lower:
            return "Nama"
        elif "caprivian" in ethnicity_lower:
            return "Caprivians"
        elif "bushman" in ethnicity_lower or "san" in ethnicity_lower:
            return "Bushmen/San"
        elif "baster" in ethnicity_lower:
            return "Basters"
        elif "tswana" in ethnicity_lower:
            return "Tswana"
        elif "coloured" in ethnicity_lower:
            return "Coloureds"
        elif "white" in ethnicity_lower and "afrikaans" in ethnicity_lower:
            return "Whites"
    
    elif country_name == "Iran (Persia)":
        if "persian" in ethnicity_lower or "farsi" in ethnicity_lower:
            return "Persians"
        elif "azerbaijani" in ethnicity_lower or "azeri" in ethnicity_lower:
            return "Azerbaijanis"
        elif "kurd" in ethnicity_lower:
            return "Kurds"
        elif "lur" in ethnicity_lower:
            return "Lurs"
        elif "gilan" in ethnicity_lower or "gilaki" in ethnicity_lower:
            return "Gilanis"
        elif "mazandarani" in ethnicity_lower:
            return "Mazandaranis"
        elif "baluch" in ethnicity_lower or "baloch" in ethnicity_lower:
            return "Baluch"
        elif "arab" in ethnicity_lower:
            return "Arabs"
        elif "turkmen" in ethnicity_lower:
            return "Turkmen"
        elif "qashqai" in ethnicity_lower:
            return "Qashqai"
        elif "bakhtiari" in ethnicity_lower:
            return "Bakhtiari"
    
    elif country_name == "Lebanon":
        if "sunni" in ethnicity_lower and "muslim" in ethnicity_lower:
            return "Sunni Muslims"
        elif "shi" in ethnicity_lower and "muslim" in ethnicity_lower:
            return "Shi'i Muslims"
        elif "maronite" in ethnicity_lower:
            return "Maronites"
        elif "greek orthodox" in ethnicity_lower:
            return "Greek Orthodox"
        elif "druze" in ethnicity_lower:
            return "Druze"
        elif "greek catholic" in ethnicity_lower:
            return "Greek Catholics"
        elif "armenian" in ethnicity_lower:
            return "Armenians"
        elif "protestant" in ethnicity_lower:
            return "Protestants"
        elif "jewish" in ethnicity_lower:
            return "Jews"
        elif "catholic" in ethnicity_lower:
            return "Catholics"
    
    elif country_name == "Ethiopia":
        if "oromo" in ethnicity_lower:
            return "Oromo"
        elif "amhara" in ethnicity_lower:
            return "Amhara"
        elif "tigray" in ethnicity_lower or "tigrinya" in ethnicity_lower:
            return "Tigray"
        elif "somali" in ethnicity_lower:
            return "Somali"
        elif "afar" in ethnicity_lower:
            return "Afar"
        elif "sidama" in ethnicity_lower:
            return "Sidama"
        elif "welayta" in ethnicity_lower or "wolayta" in ethnicity_lower:
            return "Welayta"
        elif "gurage" in ethnicity_lower:
            return "Gurage"
        elif "hadya" in ethnicity_lower:
            return "Hadya"
        elif "gamo" in ethnicity_lower:
            return "Gamo"
    
    elif country_name == "Vietnam, Democratic Republic of":
        if "vietnamese" in ethnicity_lower or "viet" in ethnicity_lower or "kinh" in ethnicity_lower:
            return "Kinh (Vietnamese)"  # EPR group name
        elif "tay" in ethnicity_lower:
            return "Tay"
        elif "thai" in ethnicity_lower and "vietnam" in ethnicity_lower:
            return "Thai"
        elif "muong" in ethnicity_lower:
            return "Muong"
        elif "khmer" in ethnicity_lower:
            return "Khmer"
        elif "hoa" in ethnicity_lower or "chinese" in ethnicity_lower:
            return "Hoa (Chinese)"
        elif "nung" in ethnicity_lower:
            return "Nung"
        elif "hmong" in ethnicity_lower:
            return "Hmong"
        elif "dao" in ethnicity_lower:
            return "Dao"
        elif "gia rai" in ethnicity_lower or "jarai" in ethnicity_lower:
            return "Gia Rai"
    
    elif country_name == "Botswana":
        if "tswana" in ethnicity_lower:
            return "Tswana"
        elif "kalanga" in ethnicity_lower:
            return "Kalanga"
        elif "bushman" in ethnicity_lower or "san" in ethnicity_lower:
            return "Bushmen/San"
        elif "herero" in ethnicity_lower:
            return "Herero"
        elif "mbukushu" in ethnicity_lower:
            return "Mbukushu"
        elif "yeyi" in ethnicity_lower:
            return "Yeyi"
        elif "white" in ethnicity_lower:
            return "Whites"
        elif "coloured" in ethnicity_lower:
            return "Coloureds"
        elif "kgalagadi" in ethnicity_lower:
            return "Kgalagadi"
    
    elif country_name == "Uganda":
        if "baganda" in ethnicity_lower or "ganda" in ethnicity_lower:
            return "Baganda"
        elif "banyankole" in ethnicity_lower or "ankole" in ethnicity_lower:
            return "Banyankole"
        elif "basoga" in ethnicity_lower or "soga" in ethnicity_lower:
            return "Basoga"
        elif "bakiga" in ethnicity_lower or "kiga" in ethnicity_lower:
            return "Bakiga"
        elif "langi" in ethnicity_lower:
            return "Langi"
        elif "acholi" in ethnicity_lower:
            return "Acholi"
        elif "lugbara" in ethnicity_lower:
            return "Lugbara"
        elif "karamojong" in ethnicity_lower:
            return "Karamojong"
        elif "teso" in ethnicity_lower:
            return "Teso"
        elif "banyoro" in ethnicity_lower or "nyoro" in ethnicity_lower:
            return "Banyoro"
    
    elif country_name == "Pakistan":
        if "punjabi" in ethnicity_lower:
            return "Punjabis"
        elif "pashtun" in ethnicity_lower or "pathan" in ethnicity_lower:
            return "Pashtuns"
        elif "sindhi" in ethnicity_lower:
            return "Sindhis"
        elif "baloch" in ethnicity_lower or "baluch" in ethnicity_lower:
            return "Baloch"
        elif "saraiki" in ethnicity_lower:
            return "Saraiki"
        elif "muhajir" in ethnicity_lower:
            return "Muhajirs"
        elif "hazara" in ethnicity_lower:
            return "Hazaras"
        elif "brahui" in ethnicity_lower:
            return "Brahui"
    
    elif country_name == "Kenya":
        if "meru" in ethnicity_lower:
            return "Kikuyu-Meru-Emb"
        
        if "kikuyu" in ethnicity_lower:
            return "Kikuyu-Meru-Emb"  # EPR group name
        elif "luhya" in ethnicity_lower:
            return "Luhya"
        elif "luo" in ethnicity_lower:
            return "Luo"
        elif "kalenjin" in ethnicity_lower:
            return "Kalenjin"
        elif "kamba" in ethnicity_lower:
            return "Kamba"
        elif "kisii" in ethnicity_lower or "gusii" in ethnicity_lower:
            return "Kisii"
        elif "meru" in ethnicity_lower:
            return "Meru"
        elif "mijikenda" in ethnicity_lower:
            return "Mijikenda"
        elif "turkana" in ethnicity_lower:
            return "Turkana"
        elif "masai" in ethnicity_lower or "maasai" in ethnicity_lower:
            return "Masai"
        elif "mara" in ethnicity_lower:
            return "Masai"  # Masai are also called Maasai/Mara
    
    elif country_name == "Serbia":
        if "serb" in ethnicity_lower:
            return "Serbs"
        elif "hungarian" in ethnicity_lower:
            return "Hungarians"
        elif "bosniak" in ethnicity_lower:
            return "Bosniaks"
        elif "romani" in ethnicity_lower or "roma" in ethnicity_lower:
            return "Roma"
        elif "croat" in ethnicity_lower:
            return "Croats"
        elif "slovak" in ethnicity_lower:
            return "Slovaks"
        elif "romanian" in ethnicity_lower:
            return "Romanians"
        elif "bulgarian" in ethnicity_lower:
            return "Bulgarians"
    
    elif country_name == "Central African Republic":
        if "gbaya" in ethnicity_lower:
            return "Gbaya"
        elif "banda" in ethnicity_lower:
            return "Banda"
        elif "mandjia" in ethnicity_lower:
            return "Mandjia"
        elif "sara" in ethnicity_lower:
            return "Sara"
        elif "mbaka" in ethnicity_lower:
            return "Mbaka"
        elif "yakoma" in ethnicity_lower:
            return "Yakoma"
        elif "ngbandi" in ethnicity_lower:
            return "Ngbandi"
    
    elif country_name == "Macedonia (FYROM/North Macedonia)":
        if "macedonian" in ethnicity_lower:
            return "Macedonians"
        elif "albanian" in ethnicity_lower:
            return "Albanians"
        elif "turk" in ethnicity_lower:
            return "Turks"
        elif "romani" in ethnicity_lower or "roma" in ethnicity_lower:
            return "Roma"
        elif "serb" in ethnicity_lower:
            return "Serbs"
        elif "bosniak" in ethnicity_lower:
            return "Bosniaks"
    
    elif country_name == "Zambia":
        if "bemba" in ethnicity_lower:
            return "Bemba"
        elif "tonga" in ethnicity_lower:
            return "Tonga"
        elif "lozi" in ethnicity_lower:
            return "Lozi"
        elif "chewa" in ethnicity_lower or "nyanja" in ethnicity_lower:
            return "Chewa/Nyanja"
        elif "nsenga" in ethnicity_lower:
            return "Nsenga"
        elif "tumbuka" in ethnicity_lower:
            return "Tumbuka"
        elif "lunda" in ethnicity_lower:
            return "Lunda"
        elif "kaonde" in ethnicity_lower:
            return "Kaonde"
        elif "luvale" in ethnicity_lower:
            return "Luvale"
        elif "lala" in ethnicity_lower:
            return "Lala"
    
    elif country_name == "Mauritius":
        if "indo-mauritian" in ethnicity_lower or "hindu" in ethnicity_lower:
            return "Indo-Mauritians"
        elif "creole" in ethnicity_lower:
            return "Creoles"
        elif "sino-mauritian" in ethnicity_lower or "chinese" in ethnicity_lower:
            return "Sino-Mauritians"
        elif "franco-mauritian" in ethnicity_lower:
            return "Franco-Mauritians"
        elif "muslim" in ethnicity_lower:
            return "Muslims"
    
    elif country_name == "Afghanistan":
        if "pashtun" in ethnicity_lower or "pathan" in ethnicity_lower:
            return "Pashtuns"
        elif "tajik" in ethnicity_lower:
            return "Tajiks"
        elif "hazara" in ethnicity_lower:
            return "Hazaras"
        elif "uzbek" in ethnicity_lower:
            return "Uzbeks"
        elif "aimak" in ethnicity_lower:
            return "Aimak"
        elif "turkmen" in ethnicity_lower:
            return "Turkmen"
        elif "baloch" in ethnicity_lower or "baluch" in ethnicity_lower:
            return "Baloch"
        elif "nuristani" in ethnicity_lower:
            return "Nuristani"
        elif "pashai" in ethnicity_lower:
            return "Pashai"
    
    # Albania patterns
    elif country_name == "Albania":
        if "albanian" in ethnicity_lower:
            return "Albanians"
        
        if "albanian" in ethnicity_lower:
            return "Albanians"
        if "greek" in ethnicity_lower:
            return "Greeks"
        if "macedonian" in ethnicity_lower:
            return "Macedonians"
    # Algeria patterns
    elif country_name == "Algeria":
        if "arab" in ethnicity_lower:
            return "Arabs"
        if "berber" in ethnicity_lower:
            return "Berbers"
    # Angola patterns
    elif country_name == "Angola":
        if "bakongo" in ethnicity_lower:
            return "Bakongo"
        if "cabindan mayombe" in ethnicity_lower:
            return "Cabindan Mayombe"
        if "lunda-chokwe" in ethnicity_lower:
            return "Lunda-Chokwe"
        if "mbundu-mestico" in ethnicity_lower:
            return "Mbundu-Mestico"
        if "ovimbundu-ovambo" in ethnicity_lower:
            return "Ovimbundu-Ovambo"
    # Argentina patterns
    elif country_name == "Argentina":
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Armenia patterns
    elif country_name == "Armenia":
        if "armenian" in ethnicity_lower:
            return "Armenians"
        if "assyrians" in ethnicity_lower:
            return "Assyrians"
        if "kurds/yezidis" in ethnicity_lower:
            return "Kurds/Yezidis"
    # Australia patterns
    elif country_name == "Australia":
        if "aboriginal" in ethnicity_lower:
            return "Aboriginal people"
        
        if "aboriginal people" in ethnicity_lower:
            return "Aboriginal people"
        if "asians" in ethnicity_lower:
            return "Asians"
        if "whites" in ethnicity_lower:
            return "Whites"
    # Austria patterns
    elif country_name == "Austria":
        if "austrian" in ethnicity_lower:
            return "Austrians"
        
        if "austrian" in ethnicity_lower:
            return "Austrians"
        if "slovenes" in ethnicity_lower:
            return "Slovenes"
    # Azerbaijan patterns
    elif country_name == "Azerbaijan":
        if "azerbaijani" in ethnicity_lower or "azerbaijani" in ethnicity_lower:
            return "Azeri"
        
        if "armenian" in ethnicity_lower:
            return "Armenians"
        if "azeri" in ethnicity_lower:
            return "Azeri"
        if "lezgins" in ethnicity_lower:
            return "Lezgins"
        if "talysh" in ethnicity_lower:
            return "Talysh"
    # Bahamas patterns
    elif country_name == "Bahamas":
        if "afro-bahamians" in ethnicity_lower:
            return "Afro-Bahamians"
        if "whites" in ethnicity_lower:
            return "Whites"
    # Bahrain patterns
    elif country_name == "Bahrain":
        if "shi'a arabs" in ethnicity_lower:
            return "Shi'a Arabs"
        if "sunni arabs" in ethnicity_lower:
            return "Sunni Arabs"
    # Bangladesh patterns
    elif country_name == "Bangladesh":
        if "bengali muslim" in ethnicity_lower or "bengali muslims" in ethnicity_lower:
            return "Bengali Muslims"
        elif "bengali hindu" in ethnicity_lower or "bengali hindus" in ethnicity_lower:
            return "Bengali Hindus"
        elif "bihari" in ethnicity_lower or "biharis" in ethnicity_lower:
            return "Biharis"
        elif "tribal-buddhist" in ethnicity_lower or "tribal-buddhists" in ethnicity_lower:
            return "Tribal-Buddhists"
        elif "bengali" in ethnicity_lower:
            return "Bengali Muslims"  # Default to Muslims (majority)
    # Barbados patterns
    elif country_name == "Barbados":
        if "barbadians" in ethnicity_lower:
            return "Barbadians"
    # Belarus (Byelorussia) patterns
    elif country_name == "Belarus (Byelorussia)":
        if "byelorussians" in ethnicity_lower:
            return "Byelorussians"
        if "poles" in ethnicity_lower:
            return "Poles"
        if "russians" in ethnicity_lower:
            return "Russians"
    # Belgium patterns
    elif country_name == "Belgium":
        if "flemings" in ethnicity_lower:
            return "Flemings"
        if "germans" in ethnicity_lower:
            return "Germans"
        if "walloon" in ethnicity_lower:
            return "Walloon"
    # Belize patterns
    elif country_name == "Belize":
        if "mestizo" in ethnicity_lower:
            return "Mestizos"
        elif "creoles" in ethnicity_lower:
            return "Creoles"
        if "garifuna" in ethnicity_lower:
            return "Garifuna"
        if "maya" in ethnicity_lower:
            return "Maya"
        if "mestizos" in ethnicity_lower:
            return "Mestizos"
    # Benin patterns
    elif country_name == "Benin":
        if "northern" in ethnicity_lower:
            return "Northern"
        if "south/central" in ethnicity_lower:
            return "South/Central"
        if "southeastern" in ethnicity_lower:
            return "Southeastern"
        if "southwestern" in ethnicity_lower:
            return "Southwestern"
    # Bhutan patterns
    elif country_name == "Bhutan":
        if "sharchop" in ethnicity_lower:
            return "Sharchops"
        
        if "lhotsampa" in ethnicity_lower:
            return "Lhotsampa"
        if "ngalops" in ethnicity_lower:
            return "Ngalops"
        if "sharchops" in ethnicity_lower:
            return "Sharchops"
    # Bolivia patterns
    elif country_name == "Bolivia":
        if "aymara" in ethnicity_lower:
            return "Aymara"
        if "guaraní and other eastern indigenous groups" in ethnicity_lower:
            return "Guaraní and other eastern indigenous groups"
        if "quechua" in ethnicity_lower:
            return "Quechua"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Bosnia-Herzegovina patterns
    elif country_name == "Bosnia-Herzegovina":
        if "bosniaks/muslims" in ethnicity_lower:
            return "Bosniaks/Muslims"
        if "croats" in ethnicity_lower:
            return "Croats"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "serbs" in ethnicity_lower:
            return "Serbs"
    # Brazil patterns
    elif country_name == "Brazil":
        if "white" in ethnicity_lower:
            return "Whites"
        if "white" in ethnicity_lower:
            return "Whites"
        
        if "afrobrazilians" in ethnicity_lower:
            return "Afrobrazilians"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "whites" in ethnicity_lower:
            return "Whites"
    # Brunei patterns
    elif country_name == "Brunei":
        if "bumiputera" in ethnicity_lower:
            return "Bumiputera"
        if "chinese" in ethnicity_lower:
            return "Chinese"
        if "non-bumiputera" in ethnicity_lower:
            return "Non-Bumiputera"
    # Bulgaria patterns
    elif country_name == "Bulgaria":
        if "bulgarians" in ethnicity_lower:
            return "Bulgarians"
        if "macedonian" in ethnicity_lower:
            return "Macedonians"
        if "pomaks" in ethnicity_lower:
            return "Pomaks"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "turkish" in ethnicity_lower:
            return "Turkish"
    # Burkina Faso (Upper Volta) patterns
    elif country_name == "Burkina Faso (Upper Volta)":
        if "gur" in ethnicity_lower:
            return "Gur"
    # Burundi patterns
    elif country_name == "Burundi":
        if "hutu" in ethnicity_lower:
            return "Hutu"
        if "tutsi" in ethnicity_lower:
            return "Tutsi"
    # Cambodia (Kampuchea) patterns
    elif country_name == "Cambodia (Kampuchea)":
        if "cham and malays" in ethnicity_lower:
            return "Cham and Malays"
        if "chinese" in ethnicity_lower:
            return "Chinese"
        if "khmer" in ethnicity_lower:
            return "Khmer"
        if "khmer loeu" in ethnicity_lower:
            return "Khmer Loeu"
        if "thai-lao" in ethnicity_lower:
            return "Thai-Lao"
        if "vietnamese" in ethnicity_lower:
            return "Vietnamese"
    # Cameroon patterns
    elif country_name == "Cameroon":
        if "bamileke" in ethnicity_lower:
            return "Bamileke"
        if "bassa/duala" in ethnicity_lower:
            return "Bassa/Duala"
        if "beti" in ethnicity_lower:
            return "Beti"
        if "fulani" in ethnicity_lower:
            return "Fulani (and other northern Muslim peoples)"
        if "northwestern anglophones" in ethnicity_lower:
            return "Northwestern Anglophones"
        if "southwestern anglophones" in ethnicity_lower:
            return "Southwestern Anglophones"
    # Canada patterns
    elif country_name == "Canada":
        if "french" in ethnicity_lower:
            return "French speakers"
        
        if "english speakers" in ethnicity_lower:
            return "English speakers"
        if "french speakers" in ethnicity_lower:
            return "French speakers"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
    # Cape Verde patterns
    elif country_name == "Cape Verde":
        if "cape" in ethnicity_lower:
            return "Cape Verdeans"
        
        if "cape verdeans" in ethnicity_lower:
            return "Cape Verdeans"
    # Chad patterns
    elif country_name == "Chad":
        if "arab" in ethnicity_lower:
            return "Arabs"
        if "hadjerai" in ethnicity_lower:
            return "Hadjerai"
        if "sara" in ethnicity_lower:
            return "Sara"
        if "tama" in ethnicity_lower:
            return "Tama"
        if "toubou" in ethnicity_lower:
            return "Toubou"
        if "zaghawa, bideyat" in ethnicity_lower:
            return "Zaghawa, Bideyat"
    # Chile patterns
    elif country_name == "Chile":
        if "mapuche" in ethnicity_lower:
            return "Mapuche"
        if "other indigenous groups" in ethnicity_lower:
            return "Other indigenous groups"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Colombia patterns
    elif country_name == "Colombia":
        if "mestizo" in ethnicity_lower:
            return "Whites/mestizos"
        if "mestizo" in ethnicity_lower:
            return "Whites/mestizos"
        
        if "afro-colombian" in ethnicity_lower:
            return "Afro-Colombian"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Comoros patterns
    elif country_name == "Comoros":
        if "mwali comorans" in ethnicity_lower:
            return "Mwali Comorans"
        if "ngazidja comorans" in ethnicity_lower:
            return "Ngazidja Comorans"
        if "nzwani comorans" in ethnicity_lower:
            return "Nzwani Comorans"
    # Congo patterns
    elif country_name == "Congo":
        if "batéké" in ethnicity_lower:
            return "Batéké"
        if "bembe" in ethnicity_lower:
            return "Bembe"
        if "kouyou" in ethnicity_lower:
            return "Kouyou"
        if "lari/bakongo" in ethnicity_lower:
            return "Lari/Bakongo"
        if "mbochi" in ethnicity_lower:
            return "Mbochi"
        if "vili" in ethnicity_lower:
            return "Vili"
    # Costa Rica patterns
    elif country_name == "Costa Rica":
        if "costa" in ethnicity_lower:
            return "Afro-Costa Ricans"
        
        if "afro-costa ricans" in ethnicity_lower:
            return "Afro-Costa Ricans"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Cote D'Ivoire patterns
    elif country_name == "Cote D'Ivoire":
        if "baule" in ethnicity_lower:
            return "Baule"
        if "kru" in ethnicity_lower:
            return "Kru"
        if "northerners" in ethnicity_lower:
            return "Northerners"
        if "other akans" in ethnicity_lower:
            return "Other Akans"
        if "southern mande" in ethnicity_lower:
            return "Southern Mande"
    # Croatia patterns
    elif country_name == "Croatia":
        if "croat" in ethnicity_lower:
            return "Croats"
        
        if "bosniaks" in ethnicity_lower:
            return "Bosniaks"
        if "croats" in ethnicity_lower:
            return "Croats"
        if "hungarian" in ethnicity_lower:
            return "Hungarians"
        if "italians" in ethnicity_lower:
            return "Italians"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "serbs" in ethnicity_lower:
            return "Serbs"
    # Cuba patterns
    elif country_name == "Cuba":
        if "cuban" in ethnicity_lower:
            return "Afro-Cubans"
        
        if "afro-cubans" in ethnicity_lower:
            return "Afro-Cubans"
        if "whites" in ethnicity_lower:
            return "Whites"
    # Cyprus patterns
    elif country_name == "Cyprus":
        if "greek" in ethnicity_lower:
            return "Greeks"
        
        if "greek" in ethnicity_lower:
            return "Greeks"
        if "turks" in ethnicity_lower:
            return "Turks"
    # Czech Republic patterns
    elif country_name == "Czech Republic":
        if "czechs" in ethnicity_lower:
            return "Czechs"
    # Denmark patterns
    elif country_name == "Denmark":
        if "danes" in ethnicity_lower:
            return "Danes"
    # Djibouti patterns
    elif country_name == "Djibouti":
        if "afar" in ethnicity_lower:
            return "Afar"
        if "isaas" in ethnicity_lower:
            return "Isaas"
    # Dominican Republic patterns
    elif country_name == "Dominican Republic":
        if "dominicans" in ethnicity_lower:
            return "Dominicans"
    # East Timor patterns
    elif country_name == "East Timor":
        if "east timorese" in ethnicity_lower:
            return "East Timorese"
    # Ecuador patterns
    elif country_name == "Ecuador":
        if "highland" in ethnicity_lower:
            return "Indigenous highland peoples (Kichwa)"
        
        if "mestizo" in ethnicity_lower:
            return "Whites/mestizos"
        if "mestizo" in ethnicity_lower:
            return "Whites/mestizos"
        if "mestizo" in ethnicity_lower:
            return "Whites/mestizos"
        
        if "afro-ecuadorian" in ethnicity_lower:
            return "Afro-Ecuadorians"
        
        if "afro-ecuadorians" in ethnicity_lower:
            return "Afro-Ecuadorians"
        if "indigenous highland peoples" in ethnicity_lower:
            return "Indigenous highland peoples"
        if "indigenous lowland peoples" in ethnicity_lower:
            return "Indigenous lowland peoples"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Egypt patterns
    elif country_name == "Egypt":
        if "coptic" in ethnicity_lower:
            return "Coptic Christians"
        
        if "arab" in ethnicity_lower:
            return "Arab Muslims"
        elif "arab muslims" in ethnicity_lower:
            return "Arab Muslims"
        if "coptic christians" in ethnicity_lower:
            return "Coptic Christians"
    # El Salvador patterns
    elif country_name == "El Salvador":
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Equatorial Guinea patterns
    elif country_name == "Equatorial Guinea":
        if "annobon islanders" in ethnicity_lower:
            return "Annobon Islanders"
        if "bubi" in ethnicity_lower:
            return "Bubi"
        if "fang" in ethnicity_lower:
            return "Fang"
        if "fernandinos" in ethnicity_lower:
            return "Fernandinos"
        if "ndowe" in ethnicity_lower:
            return "Ndowe"
    # Eritrea patterns
    elif country_name == "Eritrea":
        if "afar" in ethnicity_lower:
            return "Afar"
        if "christians" in ethnicity_lower:
            return "Christians"
        if "kunama" in ethnicity_lower:
            return "Kunama"
        if "other muslims" in ethnicity_lower:
            return "Other Muslims"
        if "saho" in ethnicity_lower:
            return "Saho"
    # Estonia patterns
    elif country_name == "Estonia":
        if "byelorussians" in ethnicity_lower:
            return "Byelorussians"
        if "estonians" in ethnicity_lower:
            return "Estonians"
        if "russians" in ethnicity_lower:
            return "Russians"
        if "ukrainians" in ethnicity_lower:
            return "Ukrainians"
    # Fiji patterns
    elif country_name == "Fiji":
        if "fijian" in ethnicity_lower:
            return "Fijians"
        if "fijian" in ethnicity_lower:
            return "Fijians"
        
        if "fijian" in ethnicity_lower:
            return "Fijians"
        if "indians" in ethnicity_lower:
            return "Indians"
    # Finland patterns
    elif country_name == "Finland":
        if "finns" in ethnicity_lower:
            return "Finns"
        if "swedes" in ethnicity_lower:
            return "Swedes"
    # France patterns
    elif country_name == "France":
        if "basques" in ethnicity_lower:
            return "Basques"
        if "corsicans" in ethnicity_lower:
            return "Corsicans"
        if "french" in ethnicity_lower:
            return "French"
        if "roma" in ethnicity_lower:
            return "Roma"
    # Gabon patterns
    elif country_name == "Gabon":
        if "eshira/bapounou" in ethnicity_lower:
            return "Eshira/Bapounou"
        if "fang" in ethnicity_lower:
            return "Fang"
        if "mbede" in ethnicity_lower:
            return "Mbede"
        if "myene" in ethnicity_lower:
            return "Myene"
    # Gambia patterns
    elif country_name == "Gambia":
        if "aku" in ethnicity_lower:
            return "Aku"
        if "diola" in ethnicity_lower:
            return "Diola"
        if "fula" in ethnicity_lower:
            return "Fula"
        if "mandinka" in ethnicity_lower:
            return "Mandinka"
        if "wolof" in ethnicity_lower:
            return "Wolof"
    # Georgia patterns
    elif country_name == "Georgia":
        if "abkhazians" in ethnicity_lower:
            return "Abkhazians"
        if "armenian" in ethnicity_lower:
            return "Armenians"
        if "azeri" in ethnicity_lower:
            return "Azeri"
        if "georgians" in ethnicity_lower:
            return "Georgians"
        if "ossetians" in ethnicity_lower:
            return "Ossetians"
    # German Federal Republic patterns
    elif country_name == "German Federal Republic":
        if "germans" in ethnicity_lower:
            return "Germans"
    # Ghana patterns
    elif country_name == "Ghana":
        if "akan" in ethnicity_lower:
            return "Other Akans"
        
        if "asante" in ethnicity_lower:
            return "Asante"
        if "ewe" in ethnicity_lower:
            return "Ewe"
        if "ga-adangbe" in ethnicity_lower:
            return "Ga-Adangbe"
        if "northern groups" in ethnicity_lower:
            return "Northern Groups"
        if "other akans" in ethnicity_lower:
            return "Other Akans"
    # Greece patterns
    elif country_name == "Greece":
        if "greek" in ethnicity_lower:
            return "Greeks"
        
        if "greek" in ethnicity_lower:
            return "Greeks"
        if "macedonian" in ethnicity_lower:
            return "Macedonians"
        if "muslims" in ethnicity_lower:
            return "Muslims"
        if "roma" in ethnicity_lower:
            return "Roma"
    # Guatemala patterns
    elif country_name == "Guatemala":
        if "garífuna" in ethnicity_lower:
            return "Garífuna"
        if "ladinos" in ethnicity_lower:
            return "Ladinos"
        if "maya" in ethnicity_lower:
            return "Maya"
        if "xinca" in ethnicity_lower:
            return "Xinca"
    # Guinea patterns
    elif country_name == "Guinea":
        if "malinke" in ethnicity_lower:
            return "Malinke"
        if "peul" in ethnicity_lower:
            return "Peul"
        if "susu" in ethnicity_lower:
            return "Susu"
    # Guinea-Bissau patterns
    elif country_name == "Guinea-Bissau":
        if "balanta" in ethnicity_lower:
            return "Balanta"
        if "cape verdean" in ethnicity_lower:
            return "Cape Verdean"
        if "manjaco" in ethnicity_lower:
            return "Manjaco"
        if "papel" in ethnicity_lower:
            return "Papel"
    # Guyana patterns
    elif country_name == "Guyana":
        if "afro-guyanese" in ethnicity_lower:
            return "Afro-Guyanese"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "indo-guyanese" in ethnicity_lower:
            return "Indo-Guyanese"
    # Haiti patterns
    elif country_name == "Haiti":
        if "haitians" in ethnicity_lower:
            return "Haitians"
    # Honduras patterns
    elif country_name == "Honduras":
        if "garifuna" in ethnicity_lower:
            return "Garifuna"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Hungary patterns
    elif country_name == "Hungary":
        if "hungarian" in ethnicity_lower:
            return "Hungarians"
        if "hungarian" in ethnicity_lower:
            return "Hungarians"
        
        if "hungarian" in ethnicity_lower:
            return "Hungarians"
        if "roma" in ethnicity_lower:
            return "Roma"
    # Iceland patterns
    elif country_name == "Iceland":
        if "icelanders" in ethnicity_lower:
            return "Icelanders"
    # Iraq patterns
    elif country_name == "Iraq":
        if "assyrians" in ethnicity_lower:
            return "Assyrians"
        if "kurds" in ethnicity_lower:
            return "Kurds"
        if "shi'a arabs" in ethnicity_lower:
            return "Shi'a Arabs"
        if "sunni arabs" in ethnicity_lower:
            return "Sunni Arabs"
        if "turkmen" in ethnicity_lower:
            return "Turkmen"
    # Ireland patterns
    elif country_name == "Ireland":
        if "irish" in ethnicity_lower:
            return "Irish"
    # Israel patterns
    elif country_name == "Israel":
        if "israeli" in ethnicity_lower:
            return "Israeli Arabs"
        if "israeli" in ethnicity_lower:
            return "Israeli Arabs"
        if "israeli" in ethnicity_lower:
            return "Israeli Arabs"
        
        if "ashkenazim" in ethnicity_lower:
            return "Ashkenazim"
        if "israeli arabs" in ethnicity_lower:
            return "Israeli Arabs"
        if "mizrahim" in ethnicity_lower:
            return "Mizrahim"
        if "palestinian arabs" in ethnicity_lower:
            return "Palestinian Arabs"
        if "russians" in ethnicity_lower:
            return "Russians"
    # Italy/Sardinia patterns
    elif country_name == "Italy/Sardinia":
        if "aostans" in ethnicity_lower:
            return "Aostans"
        if "friulians" in ethnicity_lower:
            return "Friulians"
        if "german speakers" in ethnicity_lower:
            return "German speakers"
        if "italians" in ethnicity_lower:
            return "Italians"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "sardinians" in ethnicity_lower:
            return "Sardinians"
    # Jamaica patterns
    elif country_name == "Jamaica":
        if "jamaicans" in ethnicity_lower:
            return "Jamaicans"
    # Japan patterns
    elif country_name == "Japan":
        if "ainu" in ethnicity_lower:
            return "Ainu"
        if "burakumin" in ethnicity_lower:
            return "Burakumin"
        if "japanese" in ethnicity_lower:
            return "Japanese"
        if "koreans" in ethnicity_lower:
            return "Koreans"
        if "okinawans" in ethnicity_lower:
            return "Okinawans"
    # Jordan patterns
    elif country_name == "Jordan":
        if "jordanian" in ethnicity_lower:
            return "Jordanian Arabs"
        
        if "christians" in ethnicity_lower:
            return "Christians"
        if "jordanian arabs" in ethnicity_lower:
            return "Jordanian Arabs"
        if "palestinian arabs" in ethnicity_lower:
            return "Palestinian Arabs"
    # Kazakhstan patterns
    elif country_name == "Kazakhstan":
        if "germans" in ethnicity_lower:
            return "Germans"
        if "kazakhs" in ethnicity_lower:
            return "Kazakhs"
        if "russian-speakers" in ethnicity_lower:
            return "Russian-speakers"
        if "tatars" in ethnicity_lower:
            return "Tatars"
        if "uighur" in ethnicity_lower:
            return "Uighur"
        if "uzbeks" in ethnicity_lower:
            return "Uzbeks"
    # Korea, People's Republic of patterns
    elif country_name == "Korea, People's Republic of":
        if "koreans" in ethnicity_lower:
            return "Koreans"
    # Korea, Republic of patterns
    elif country_name == "Korea, Republic of":
        if "koreans" in ethnicity_lower:
            return "Koreans"
    # Kosovo patterns
    elif country_name == "Kosovo":
        if "albanian" in ethnicity_lower:
            return "Albanians"
        if "bosniaks" in ethnicity_lower:
            return "Bosniaks"
        if "gorani" in ethnicity_lower:
            return "Gorani"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "serbs" in ethnicity_lower:
            return "Serbs"
        if "turks" in ethnicity_lower:
            return "Turks"
    # Kuwait patterns
    elif country_name == "Kuwait":
        if "bedoon" in ethnicity_lower:
            return "Bedoon"
        if "kuwaiti shi'a" in ethnicity_lower:
            return "Kuwaiti Shi'a"
        if "kuwaiti sunni" in ethnicity_lower:
            return "Kuwaiti Sunni"
    # Kyrgyz Republic patterns
    elif country_name == "Kyrgyz Republic":
        if "kyrgyz" in ethnicity_lower:
            return "Kyrgyz"
        if "russians" in ethnicity_lower:
            return "Russians"
        if "uyghur" in ethnicity_lower:
            return "Uyghur"
        if "uzbeks" in ethnicity_lower:
            return "Uzbeks"
    # Laos patterns
    elif country_name == "Laos":
        if "hmong" in ethnicity_lower:
            return "Hmong"
        if "khmou" in ethnicity_lower:
            return "Khmou"
        if "lao" in ethnicity_lower:
            return "Lao"
        if "lao sung" in ethnicity_lower:
            return "Lao Sung"
        if "lao tai" in ethnicity_lower:
            return "Lao Tai"
        if "lao thoeng" in ethnicity_lower:
            return "Lao Thoeng"
    # Latvia patterns
    elif country_name == "Latvia":
        if "byelorussians" in ethnicity_lower:
            return "Byelorussians"
        if "latvians" in ethnicity_lower:
            return "Latvians"
        if "russians" in ethnicity_lower:
            return "Russians"
        if "ukrainians" in ethnicity_lower:
            return "Ukrainians"
    # Lesotho patterns
    elif country_name == "Lesotho":
        if "sotho" in ethnicity_lower:
            return "Sotho"
    # Liberia patterns
    elif country_name == "Liberia":
        if "americo-liberians" in ethnicity_lower:
            return "Americo-Liberians"
        if "gio" in ethnicity_lower:
            return "Gio"
        if "krahn" in ethnicity_lower:
            return "Krahn"
        if "kru" in ethnicity_lower:
            return "Kru"
        if "mandingo" in ethnicity_lower:
            return "Mandingo"
        if "mano" in ethnicity_lower:
            return "Mano"
    # Libya patterns
    elif country_name == "Libya":
        if "arab" in ethnicity_lower:
            return "Arabs"
        if "berber" in ethnicity_lower:
            return "Berbers"
        if "toubou" in ethnicity_lower:
            return "Toubou"
        if "tuareg" in ethnicity_lower:
            return "Tuareg"
    # Lithuania patterns
    elif country_name == "Lithuania":
        if "lithuanians" in ethnicity_lower:
            return "Lithuanians"
        if "poles" in ethnicity_lower:
            return "Poles"
        if "russians" in ethnicity_lower:
            return "Russians"
    # Luxembourg patterns
    elif country_name == "Luxembourg":
        if "luxembourger" in ethnicity_lower:
            return "Luxembourgers"
        
        if "luxembourger" in ethnicity_lower:
            return "Luxembourgers"
    # Madagascar (Malagasy) patterns
    elif country_name == "Madagascar (Malagasy)":
        if "côtiers" in ethnicity_lower:
            return "Côtiers"
        if "highlanders" in ethnicity_lower:
            return "Highlanders"
    # Malawi patterns
    elif country_name == "Malawi":
        if "central" in ethnicity_lower:
            return "Central"
        if "northerners" in ethnicity_lower:
            return "Northerners"
        if "southerners" in ethnicity_lower:
            return "Southerners"
    # Malaysia patterns
    elif country_name == "Malaysia":
        if "malay" in ethnicity_lower:
            return "Malays"
        if "malay" in ethnicity_lower:
            return "Malays"
        
        if "chinese" in ethnicity_lower:
            return "Chinese"
        if "dayaks" in ethnicity_lower:
            return "Dayaks"
        if "east indians" in ethnicity_lower:
            return "East Indians"
        if "kadazans" in ethnicity_lower:
            return "Kadazans"
        if "malays" in ethnicity_lower:
            return "Malays"
        if "orang asli" in ethnicity_lower:
            return "Orang Asli"
    # Maldives patterns
    elif country_name == "Maldives":
        if "divehis" in ethnicity_lower:
            return "Divehis"
    # Mali patterns
    elif country_name == "Mali":
        if "arabs/moors" in ethnicity_lower:
            return "Arabs/Moors"
        if "blacks" in ethnicity_lower:
            return "Blacks"
        if "tuareg" in ethnicity_lower:
            return "Tuareg"
    # Malta patterns
    elif country_name == "Malta":
        if "maltese" in ethnicity_lower:
            return "Maltese"
    # Mauritania patterns
    elif country_name == "Mauritania":
        if "black" in ethnicity_lower:
            return "Black Africans"
        if "black" in ethnicity_lower:
            return "Black Africans"
        if "white" in ethnicity_lower:
            return "White Moors (Beydan)"
        
        if "black africans" in ethnicity_lower:
            return "Black Africans"
        if "haratins" in ethnicity_lower:
            return "Haratins"
        if "white moors" in ethnicity_lower:
            return "White Moors"
    # Mexico patterns
    elif country_name == "Mexico":
        if "afromexicans" in ethnicity_lower:
            return "Afromexicans"
        if "maya" in ethnicity_lower:
            return "Maya"
        if "mestizos" in ethnicity_lower:
            return "Mestizos"
        if "other indigenous groups" in ethnicity_lower:
            return "Other indigenous groups"
    # Moldova patterns
    elif country_name == "Moldova":
        if "moldovan" in ethnicity_lower:
            return "Moldovans"
        
        if "bulgarians" in ethnicity_lower:
            return "Bulgarians"
        if "gagauz" in ethnicity_lower:
            return "Gagauz"
        if "moldovans" in ethnicity_lower:
            return "Moldovans"
        if "russian speakers" in ethnicity_lower:
            return "Russian speakers"
    # Mongolia patterns
    elif country_name == "Mongolia":
        if "kazakh" in ethnicity_lower:
            return "Kazakh"
        if "mongols" in ethnicity_lower:
            return "Mongols"
    # Montenegro patterns
    elif country_name == "Montenegro":
        if "albanian" in ethnicity_lower:
            return "Albanians"
        if "bosniak/muslims" in ethnicity_lower:
            return "Bosniak/Muslims"
        if "croats" in ethnicity_lower:
            return "Croats"
        if "montenegrins" in ethnicity_lower:
            return "Montenegrins"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "serbs" in ethnicity_lower:
            return "Serbs"
    # Morocco patterns
    elif country_name == "Morocco":
        if "arab" in ethnicity_lower:
            return "Arabs"
        if "berber" in ethnicity_lower:
            return "Berbers"
        if "sahrawis" in ethnicity_lower:
            return "Sahrawis"
    # Mozambique patterns
    elif country_name == "Mozambique":
        if "makonde-yao" in ethnicity_lower:
            return "Makonde-Yao"
        if "shona-ndau" in ethnicity_lower:
            return "Shona-Ndau"
        if "tsonga-chopi" in ethnicity_lower:
            return "Tsonga-Chopi"
    # Nepal patterns
    elif country_name == "Nepal":
        if "hill" in ethnicity_lower:
            return "Caste Hill Hindu Elite"
        
        if "adibasi" in ethnicity_lower:
            return "Adibasi Janajati"
        
        if "adibasi janajati" in ethnicity_lower:
            return "Adibasi Janajati"
        if "caste hill hindu elite" in ethnicity_lower:
            return "Caste Hill Hindu Elite"
        if "dalits" in ethnicity_lower:
            return "Dalits"
        if "madhesi" in ethnicity_lower:
            return "Madhesi"
        if "muslims" in ethnicity_lower:
            return "Muslims"
        if "newars" in ethnicity_lower:
            return "Newars"
    # Netherlands patterns
    elif country_name == "Netherlands":
        if "dutch" in ethnicity_lower:
            return "Dutch"
    # New Zealand patterns
    elif country_name == "New Zealand":
        if "zealander" in ethnicity_lower:
            return "New Zealanders"
        if "zealander" in ethnicity_lower:
            return "New Zealanders"
        if "zealander" in ethnicity_lower:
            return "New Zealanders"
        
        if "asians" in ethnicity_lower:
            return "Asians"
        if "maori" in ethnicity_lower:
            return "Maori"
        if "new zealanders" in ethnicity_lower:
            return "New Zealanders"
        if "pacific islanders" in ethnicity_lower:
            return "Pacific Islanders"
    # Nicaragua patterns
    elif country_name == "Nicaragua":
        if "afronicaraguans" in ethnicity_lower:
            return "Afronicaraguans"
        if "miskitos" in ethnicity_lower:
            return "Miskitos"
        if "sumus" in ethnicity_lower:
            return "Sumus"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Niger patterns
    elif country_name == "Niger":
        if "djerma-songhai" in ethnicity_lower:
            return "Djerma-Songhai"
        if "hausa" in ethnicity_lower:
            return "Hausa"
        if "kanouri" in ethnicity_lower:
            return "Kanouri"
        if "toubou" in ethnicity_lower:
            return "Toubou"
        if "tuareg" in ethnicity_lower:
            return "Tuareg"
    # Nigeria patterns
    elif country_name == "Nigeria":
        if "fulani" in ethnicity_lower:
            return "Hausa-Fulani and Muslim Middle Belt"
        
        if "hausa-fulani and muslim middle belt" in ethnicity_lower:
            return "Hausa-Fulani and Muslim Middle Belt"
        if "igbo" in ethnicity_lower:
            return "Igbo"
        if "ijaw" in ethnicity_lower:
            return "Ijaw"
        if "ogoni" in ethnicity_lower:
            return "Ogoni"
        if "tiv" in ethnicity_lower:
            return "Tiv"
        if "yoruba" in ethnicity_lower:
            return "Yoruba"
    # Norway patterns
    elif country_name == "Norway":
        if "norwegian" in ethnicity_lower:
            return "Norwegians"
        if "norwegian" in ethnicity_lower:
            return "Norwegians"
        if "norwegian" in ethnicity_lower:
            return "Norwegians"
        
        if "norwegians" in ethnicity_lower:
            return "Norwegians"
    # Oman patterns
    elif country_name == "Oman":
        if "ibadhi muslims" in ethnicity_lower:
            return "Ibadhi Muslims"
    # Panama patterns
    elif country_name == "Panama":
        if "afropanamanians" in ethnicity_lower:
            return "Afropanamanians"
        if "choco" in ethnicity_lower:
            return "Choco"
        if "kuna" in ethnicity_lower:
            return "Kuna"
        if "ngäbe-buglé" in ethnicity_lower:
            return "Ngäbe-Buglé"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Papua New Guinea patterns
    elif country_name == "Papua New Guinea":
        if "bougainvilleans" in ethnicity_lower:
            return "Bougainvilleans"
        if "papua new guineans" in ethnicity_lower:
            return "Papua New Guineans"
    # Paraguay patterns
    elif country_name == "Paraguay":
        if "tupi-guaraní and other indigenous groups" in ethnicity_lower:
            return "Tupi-Guaraní and other indigenous groups"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Peru patterns
    elif country_name == "Peru":
        if "peruvian" in ethnicity_lower:
            return "Afroperuvians"
        if "peruvian" in ethnicity_lower:
            return "Afroperuvians"
        if "peruvian" in ethnicity_lower:
            return "Afroperuvians"
        
        if "afroperuvians" in ethnicity_lower:
            return "Afroperuvians"
        if "indigenous peoples of the amazon" in ethnicity_lower:
            return "Indigenous peoples of the Amazon"
        if "indigenous peoples of the andes" in ethnicity_lower:
            return "Indigenous peoples of the Andes"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Philippines patterns
    elif country_name == "Philippines":
        if "christian lowlanders" in ethnicity_lower:
            return "Christian lowlanders"
        if "fil-chinese" in ethnicity_lower:
            return "Fil-Chinese"
        if "indigenous" in ethnicity_lower:
            return "Indigenous"
        if "moro" in ethnicity_lower:
            return "Moro"
    # Poland patterns
    elif country_name == "Poland":
        if "byelorussians" in ethnicity_lower:
            return "Byelorussians"
        if "european and american jews" in ethnicity_lower:
            return "European and American Jews"
        if "germans" in ethnicity_lower:
            return "Germans"
        if "poles" in ethnicity_lower:
            return "Poles"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "ukrainians" in ethnicity_lower:
            return "Ukrainians"
    # Portugal patterns
    elif country_name == "Portugal":
        if "portuguese" in ethnicity_lower:
            return "Portuguese"
    # Qatar patterns
    elif country_name == "Qatar":
        if "qatari arabs" in ethnicity_lower:
            return "Qatari Arabs"
    # Rumania patterns
    elif country_name == "Rumania":
        if "germans" in ethnicity_lower:
            return "Germans"
        if "hungarian" in ethnicity_lower:
            return "Hungarians"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "romanians" in ethnicity_lower:
            return "Romanians"
    # Rwanda patterns
    elif country_name == "Rwanda":
        if "hutu" in ethnicity_lower:
            return "Hutu"
        if "tutsi" in ethnicity_lower:
            return "Tutsi"
    # Saudi Arabia patterns
    elif country_name == "Saudi Arabia":
        if "ismaili shia" in ethnicity_lower:
            return "Ismaili Shia"
        if "ja'afari shia" in ethnicity_lower:
            return "Ja'afari Shia"
        if "sunni shafii/sofi" in ethnicity_lower:
            return "Sunni Shafii/Sofi"
        if "sunni wahhabi" in ethnicity_lower:
            return "Sunni Wahhabi"
    # Senegal patterns
    elif country_name == "Senegal":
        if "diola" in ethnicity_lower:
            return "Diola"
        if "mandingue" in ethnicity_lower:
            return "Mandingue"
        if "pulaar" in ethnicity_lower:
            return "Pulaar"
        if "serer" in ethnicity_lower:
            return "Serer"
        if "wolof" in ethnicity_lower:
            return "Wolof"
    # Sierra Leone patterns
    elif country_name == "Sierra Leone":
        if "creole" in ethnicity_lower:
            return "Creole"
        if "kono" in ethnicity_lower:
            return "Kono"
        if "limba" in ethnicity_lower:
            return "Limba"
        if "mende" in ethnicity_lower:
            return "Mende"
        if "temne" in ethnicity_lower:
            return "Temne"
    # Singapore patterns
    elif country_name == "Singapore":
        if "chinese" in ethnicity_lower:
            return "Chinese"
        if "eurasians and others" in ethnicity_lower:
            return "Eurasians and Others"
        if "indians" in ethnicity_lower:
            return "Indians"
        if "malays" in ethnicity_lower:
            return "Malays"
    # Slovakia patterns
    elif country_name == "Slovakia":
        if "hungarian" in ethnicity_lower:
            return "Hungarians"
        if "slovaks" in ethnicity_lower:
            return "Slovaks"
    # Slovenia patterns
    elif country_name == "Slovenia":
        if "hungarian" in ethnicity_lower:
            return "Hungarians"
        if "italians" in ethnicity_lower:
            return "Italians"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "slovenes" in ethnicity_lower:
            return "Slovenes"
    # Solomon Islands patterns
    elif country_name == "Solomon Islands":
        if "solomon islanders" in ethnicity_lower:
            return "Solomon Islanders"
    # Somalia patterns
    elif country_name == "Somalia":
        if "somali" in ethnicity_lower:
            return "Somali"
    # Spain patterns
    elif country_name == "Spain":
        if "basques" in ethnicity_lower:
            return "Basques"
        if "catalans" in ethnicity_lower:
            return "Catalans"
        if "galicians" in ethnicity_lower:
            return "Galicians"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "spanish" in ethnicity_lower:
            return "Spanish"
    # Sri Lanka (Ceylon) patterns
    elif country_name == "Sri Lanka (Ceylon)":
        if "indian tamils" in ethnicity_lower:
            return "Indian Tamils"
        if "moors" in ethnicity_lower:
            return "Moors"
        if "sinhalese" in ethnicity_lower:
            return "Sinhalese"
        if "sri lankan tamils" in ethnicity_lower:
            return "Sri Lankan Tamils"
    # Surinam patterns
    elif country_name == "Surinam":
        if "chinese" in ethnicity_lower:
            return "Chinese"
        if "creoles" in ethnicity_lower:
            return "Creoles"
        if "east indians" in ethnicity_lower:
            return "East Indians"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous Peoples"
        if "javanese" in ethnicity_lower:
            return "Javanese"
        if "maroons" in ethnicity_lower:
            return "Maroons"
    # Swaziland (Eswatini) patterns
    elif country_name == "Swaziland (Eswatini)":
        if "swazi" in ethnicity_lower:
            return "Swazi"
    # Sweden patterns
    elif country_name == "Sweden":
        if "swedes" in ethnicity_lower:
            return "Swedes"
    # Switzerland patterns
    elif country_name == "Switzerland":
        if "swiss french" in ethnicity_lower:
            return "Swiss French"
        if "swiss germans" in ethnicity_lower:
            return "Swiss Germans"
        if "swiss italians" in ethnicity_lower:
            return "Swiss Italians"
    # Syria patterns
    elif country_name == "Syria":
        if "alawi" in ethnicity_lower:
            return "Alawi"
        if "christians" in ethnicity_lower:
            return "Christians"
        if "druze" in ethnicity_lower:
            return "Druze"
        if "kurds" in ethnicity_lower:
            return "Kurds"
        if "sunni arabs" in ethnicity_lower:
            return "Sunni Arabs"
    # Taiwan patterns
    elif country_name == "Taiwan":
        if "indigenous/aboriginal taiwanese" in ethnicity_lower:
            return "Indigenous/Aboriginal Taiwanese"
        if "mainland chinese" in ethnicity_lower:
            return "Mainland Chinese"
        if "taiwanese" in ethnicity_lower:
            return "Taiwanese"
    # Tajikistan patterns
    elif country_name == "Tajikistan":
        if "kyrgyz" in ethnicity_lower:
            return "Kyrgyz"
        if "pamiri tajiks" in ethnicity_lower:
            return "Pamiri Tajiks"
        if "russians" in ethnicity_lower:
            return "Russians"
        if "tajiks" in ethnicity_lower:
            return "Tajiks"
        if "tatars" in ethnicity_lower:
            return "Tatars"
        if "uzbeks" in ethnicity_lower:
            return "Uzbeks"
    # Tanzania (Tanganyika) patterns
    elif country_name == "Tanzania (Tanganyika)":
        if "maasai" in ethnicity_lower:
            return "Maasai"
        if "mainland muslims" in ethnicity_lower:
            return "Mainland Muslims"
        if "others mainland" in ethnicity_lower:
            return "Others Mainland"
        if "shirazi" in ethnicity_lower:
            return "Shirazi"
        if "zanzibar arabs" in ethnicity_lower:
            return "Zanzibar Arabs"
    # Thailand patterns
    elif country_name == "Thailand":
        if "chinese" in ethnicity_lower:
            return "Chinese"
        if "hill tribes" in ethnicity_lower:
            return "Hill Tribes"
        if "malay muslims" in ethnicity_lower:
            return "Malay Muslims"
        if "shan" in ethnicity_lower:
            return "Shan"
        if "thai" in ethnicity_lower:
            return "Thai"
    # Togo patterns
    elif country_name == "Togo":
        if "ewe" in ethnicity_lower:
            return "Ewe"
        if "kabré" in ethnicity_lower:
            return "Kabré"
    # Trinidad and Tobago patterns
    elif country_name == "Trinidad and Tobago":
        if "blacks" in ethnicity_lower:
            return "Blacks"
        if "east indians" in ethnicity_lower:
            return "East Indians"
    # Tunisia patterns
    elif country_name == "Tunisia":
        if "arab" in ethnicity_lower:
            return "Arabs"
    # Turkey (Ottoman Empire) patterns
    elif country_name == "Turkey (Ottoman Empire)":
        if "kurds" in ethnicity_lower:
            return "Kurds"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "turkish" in ethnicity_lower:
            return "Turkish"
    # Turkmenistan patterns
    elif country_name == "Turkmenistan":
        if "kazakhs" in ethnicity_lower:
            return "Kazakhs"
        if "russians" in ethnicity_lower:
            return "Russians"
        if "turkmen" in ethnicity_lower:
            return "Turkmen"
        if "uzbeks" in ethnicity_lower:
            return "Uzbeks"
    # Ukraine patterns
    elif country_name == "Ukraine":
        if "crimean tatars" in ethnicity_lower:
            return "Crimean Tatars"
        if "hungarian" in ethnicity_lower:
            return "Hungarians"
        if "romanians/moldovans" in ethnicity_lower:
            return "Romanians/Moldovans"
        if "russians" in ethnicity_lower:
            return "Russians"
        if "rusyns" in ethnicity_lower:
            return "Rusyns"
        if "ukrainians" in ethnicity_lower:
            return "Ukrainians"
    # United Arab Emirates patterns
    elif country_name == "United Arab Emirates":
        if "emirati arabs" in ethnicity_lower:
            return "Emirati Arabs"
    # United Kingdom patterns
    elif country_name == "United Kingdom":
        if "afro-caribbeans" in ethnicity_lower:
            return "Afro-Caribbeans"
        if "asians" in ethnicity_lower:
            return "Asians"
        if "catholics in n. ireland" in ethnicity_lower:
            return "Catholics In N. Ireland"
        if "english" in ethnicity_lower:
            return "English"
        if "protestants in n. ireland" in ethnicity_lower:
            return "Protestants In N. Ireland"
        if "scots" in ethnicity_lower:
            return "Scots"
        if "welsh" in ethnicity_lower:
            return "Welsh"
    # United States of America patterns
    elif country_name == "United States of America":
        if "americans" in ethnicity_lower:
            return "African Americans"
        if "americans" in ethnicity_lower:
            return "African Americans"
        if "americans" in ethnicity_lower:
            return "African Americans"
        
        if "african americans" in ethnicity_lower:
            return "African Americans"
        if "american indians" in ethnicity_lower:
            return "American Indians"
        if "arab americans" in ethnicity_lower:
            return "Arab Americans"
        if "asian americans" in ethnicity_lower:
            return "Asian Americans"
        if "latinos" in ethnicity_lower:
            return "Latinos"
        if "whites" in ethnicity_lower:
            return "Whites"
    # Uruguay patterns
    elif country_name == "Uruguay":
        if "afro-uruguayans" in ethnicity_lower:
            return "Afro-Uruguayans"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Uzbekistan patterns
    elif country_name == "Uzbekistan":
        if "karakalpak" in ethnicity_lower:
            return "Karakalpak"
        if "russians" in ethnicity_lower:
            return "Russians"
        if "tajiks" in ethnicity_lower:
            return "Tajiks"
        if "uzbeks" in ethnicity_lower:
            return "Uzbeks"
    # Venezuela patterns
    elif country_name == "Venezuela":
        if "venezuelan" in ethnicity_lower:
            return "Afrovenezuelans"
        if "venezuelan" in ethnicity_lower:
            return "Afrovenezuelans"
        if "venezuelan" in ethnicity_lower:
            return "Afrovenezuelans"
        
        if "afrovenezuelans" in ethnicity_lower:
            return "Afrovenezuelans"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Yemen (Arab Republic of Yemen) patterns
    elif country_name == "Yemen (Arab Republic of Yemen)":
        if "al-akhdam" in ethnicity_lower:
            return "Al-Akhdam"
        if "northern shafi'i" in ethnicity_lower:
            return "Northern Shafi'i"
        if "northern zaydis" in ethnicity_lower:
            return "Northern Zaydis"
        if "southern shafi'i" in ethnicity_lower:
            return "Southern Shafi'i"
    # Zimbabwe (Rhodesia) patterns
    elif country_name == "Zimbabwe (Rhodesia)":
        if "ndebele-kalanga-" in ethnicity_lower:
            return "Ndebele-Kalanga-"
        if "shona" in ethnicity_lower:
            return "Shona"
        if "white zimbabweans" in ethnicity_lower:
            return "White Zimbabweans"
    
    # Albania patterns
    elif country_name == "Albania":
        if "albanian" in ethnicity_lower:
            return "Albanians"
        if "greek" in ethnicity_lower:
            return "Greeks"
        if "macedonian" in ethnicity_lower:
            return "Macedonians"
    # Algeria patterns
    elif country_name == "Algeria":
        if "arab" in ethnicity_lower:
            return "Arabs"
        if "berber" in ethnicity_lower:
            return "Berbers"
    # Angola patterns
    elif country_name == "Angola":
        if "bakongo" in ethnicity_lower:
            return "Bakongo"
        if "cabindan mayombe" in ethnicity_lower:
            return "Cabindan Mayombe"
        if "lunda-chokwe" in ethnicity_lower:
            return "Lunda-Chokwe"
        if "mbundu-mestico" in ethnicity_lower:
            return "Mbundu-Mestico"
        if "ovimbundu-ovambo" in ethnicity_lower:
            return "Ovimbundu-Ovambo"
    # Argentina patterns
    elif country_name == "Argentina":
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Armenia patterns
    elif country_name == "Armenia":
        if "armenian" in ethnicity_lower:
            return "Armenians"
        if "assyrians" in ethnicity_lower:
            return "Assyrians"
        if "kurds/yezidis" in ethnicity_lower:
            return "Kurds/Yezidis"
    # Australia patterns
    elif country_name == "Australia":
        if "aboriginal people" in ethnicity_lower:
            return "Aboriginal people"
        if "asians" in ethnicity_lower:
            return "Asians"
        if "whites" in ethnicity_lower:
            return "Whites"
    # Austria patterns
    elif country_name == "Austria":
        if "austrian" in ethnicity_lower:
            return "Austrians"
        if "slovenes" in ethnicity_lower:
            return "Slovenes"
    # Azerbaijan patterns
    elif country_name == "Azerbaijan":
        if "armenian" in ethnicity_lower:
            return "Armenians"
        elif "azerbaijani" in ethnicity_lower or "azeri" in ethnicity_lower:
            return "Azeri"
        elif "lezgins" in ethnicity_lower or "lezgin" in ethnicity_lower:
            return "Lezgins"
        elif "talysh" in ethnicity_lower:
            return "Talysh"
    # Bahamas patterns
    elif country_name == "Bahamas":
        if "afro-bahamians" in ethnicity_lower:
            return "Afro-Bahamians"
        if "whites" in ethnicity_lower:
            return "Whites"
    # Bahrain patterns
    elif country_name == "Bahrain":
        if "shi'a arabs" in ethnicity_lower:
            return "Shi'a Arabs"
        if "sunni arabs" in ethnicity_lower:
            return "Sunni Arabs"
    # Bangladesh patterns
    elif country_name == "Bangladesh":
        if "bengali muslim" in ethnicity_lower or "bengali muslims" in ethnicity_lower:
            return "Bengali Muslims"
        elif "bengali hindu" in ethnicity_lower or "bengali hindus" in ethnicity_lower:
            return "Bengali Hindus"
        elif "bihari" in ethnicity_lower or "biharis" in ethnicity_lower:
            return "Biharis"
        elif "tribal-buddhist" in ethnicity_lower or "tribal-buddhists" in ethnicity_lower:
            return "Tribal-Buddhists"
        elif "bengali" in ethnicity_lower:
            return "Bengali Muslims"  # Default to Muslims (majority)
    # Barbados patterns
    elif country_name == "Barbados":
        if "barbadians" in ethnicity_lower:
            return "Barbadians"
    # Belarus (Byelorussia) patterns
    elif country_name == "Belarus (Byelorussia)":
        if "byelorussians" in ethnicity_lower:
            return "Byelorussians"
        if "poles" in ethnicity_lower:
            return "Poles"
        if "russians" in ethnicity_lower:
            return "Russians"
    # Belgium patterns
    elif country_name == "Belgium":
        if "flemings" in ethnicity_lower:
            return "Flemings"
        if "germans" in ethnicity_lower:
            return "Germans"
        if "walloon" in ethnicity_lower:
            return "Walloon"
    # Belize patterns
    elif country_name == "Belize":
        if "creoles" in ethnicity_lower:
            return "Creoles"
        if "garifuna" in ethnicity_lower:
            return "Garifuna"
        if "maya" in ethnicity_lower:
            return "Maya"
        if "mestizos" in ethnicity_lower:
            return "Mestizos"
    # Benin patterns
    elif country_name == "Benin":
        if "northern" in ethnicity_lower:
            return "Northern"
        if "south/central" in ethnicity_lower:
            return "South/Central"
        if "southeastern" in ethnicity_lower:
            return "Southeastern"
        if "southwestern" in ethnicity_lower:
            return "Southwestern"
    # Bhutan patterns
    elif country_name == "Bhutan":
        if "lhotsampa" in ethnicity_lower:
            return "Lhotsampa"
        if "ngalops" in ethnicity_lower:
            return "Ngalops"
        if "sharchops" in ethnicity_lower:
            return "Sharchops"
    # Bolivia patterns
    elif country_name == "Bolivia":
        if "aymara" in ethnicity_lower:
            return "Aymara"
        if "guaraní and other eastern indigenous groups" in ethnicity_lower:
            return "Guaraní and other eastern indigenous groups"
        if "quechua" in ethnicity_lower:
            return "Quechua"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Bosnia-Herzegovina patterns
    elif country_name == "Bosnia-Herzegovina":
        if "bosniaks/muslims" in ethnicity_lower:
            return "Bosniaks/Muslims"
        if "croats" in ethnicity_lower:
            return "Croats"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "serbs" in ethnicity_lower:
            return "Serbs"
    # Brazil patterns
    elif country_name == "Brazil":
        if "afrobrazilians" in ethnicity_lower:
            return "Afrobrazilians"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "whites" in ethnicity_lower:
            return "Whites"
    # Brunei patterns
    elif country_name == "Brunei":
        if "bumiputera" in ethnicity_lower:
            return "Bumiputera"
        if "chinese" in ethnicity_lower:
            return "Chinese"
        if "non-bumiputera" in ethnicity_lower:
            return "Non-Bumiputera"
    # Bulgaria patterns
    elif country_name == "Bulgaria":
        if "bulgarians" in ethnicity_lower:
            return "Bulgarians"
        if "macedonian" in ethnicity_lower:
            return "Macedonians"
        if "pomaks" in ethnicity_lower:
            return "Pomaks"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "turkish" in ethnicity_lower:
            return "Turkish"
    # Burkina Faso (Upper Volta) patterns
    elif country_name == "Burkina Faso (Upper Volta)":
        if "gur" in ethnicity_lower:
            return "Gur"
    # Burundi patterns
    elif country_name == "Burundi":
        if "hutu" in ethnicity_lower:
            return "Hutu"
        if "tutsi" in ethnicity_lower:
            return "Tutsi"
    # Cambodia (Kampuchea) patterns
    elif country_name == "Cambodia (Kampuchea)":
        if "cham and malays" in ethnicity_lower:
            return "Cham and Malays"
        if "chinese" in ethnicity_lower:
            return "Chinese"
        if "khmer" in ethnicity_lower:
            return "Khmer"
        if "khmer loeu" in ethnicity_lower:
            return "Khmer Loeu"
        if "thai-lao" in ethnicity_lower:
            return "Thai-Lao"
        if "vietnamese" in ethnicity_lower:
            return "Vietnamese"
    # Cameroon patterns
    elif country_name == "Cameroon":
        if "bamileke" in ethnicity_lower:
            return "Bamileke"
        if "bassa/duala" in ethnicity_lower:
            return "Bassa/Duala"
        if "beti" in ethnicity_lower:
            return "Beti"
        if "fulani" in ethnicity_lower:
            return "Fulani"
        if "northwestern anglophones" in ethnicity_lower:
            return "Northwestern Anglophones"
        if "southwestern anglophones" in ethnicity_lower:
            return "Southwestern Anglophones"
    # Canada patterns
    elif country_name == "Canada":
        if "english speakers" in ethnicity_lower:
            return "English speakers"
        if "french speakers" in ethnicity_lower:
            return "French speakers"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
    # Cape Verde patterns
    elif country_name == "Cape Verde":
        if "cape verdeans" in ethnicity_lower:
            return "Cape Verdeans"
    # Chad patterns
    elif country_name == "Chad":
        if "arab" in ethnicity_lower:
            return "Arabs"
        if "hadjerai" in ethnicity_lower:
            return "Hadjerai"
        if "sara" in ethnicity_lower:
            return "Sara"
        if "tama" in ethnicity_lower:
            return "Tama"
        if "toubou" in ethnicity_lower:
            return "Toubou"
        if "zaghawa, bideyat" in ethnicity_lower:
            return "Zaghawa, Bideyat"
    # Chile patterns
    elif country_name == "Chile":
        if "mapuche" in ethnicity_lower:
            return "Mapuche"
        if "other indigenous groups" in ethnicity_lower:
            return "Other indigenous groups"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Colombia patterns
    elif country_name == "Colombia":
        if "afro-colombian" in ethnicity_lower:
            return "Afro-Colombian"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Comoros patterns
    elif country_name == "Comoros":
        if "mwali comorans" in ethnicity_lower:
            return "Mwali Comorans"
        if "ngazidja comorans" in ethnicity_lower:
            return "Ngazidja Comorans"
        if "nzwani comorans" in ethnicity_lower:
            return "Nzwani Comorans"
    # Congo patterns
    elif country_name == "Congo":
        if "batéké" in ethnicity_lower:
            return "Batéké"
        if "bembe" in ethnicity_lower:
            return "Bembe"
        if "kouyou" in ethnicity_lower:
            return "Kouyou"
        if "lari/bakongo" in ethnicity_lower:
            return "Lari/Bakongo"
        if "mbochi" in ethnicity_lower:
            return "Mbochi"
        if "vili" in ethnicity_lower:
            return "Vili"
    # Costa Rica patterns
    elif country_name == "Costa Rica":
        if "afro-costa ricans" in ethnicity_lower:
            return "Afro-Costa Ricans"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Cote D'Ivoire patterns
    elif country_name == "Cote D'Ivoire":
        if "baule" in ethnicity_lower:
            return "Baule"
        if "kru" in ethnicity_lower:
            return "Kru"
        if "northerners" in ethnicity_lower:
            return "Northerners"
        if "other akans" in ethnicity_lower:
            return "Other Akans"
        if "southern mande" in ethnicity_lower:
            return "Southern Mande"
    # Croatia patterns
    elif country_name == "Croatia":
        if "bosniaks" in ethnicity_lower:
            return "Bosniaks"
        if "croats" in ethnicity_lower:
            return "Croats"
        if "hungarian" in ethnicity_lower:
            return "Hungarians"
        if "italians" in ethnicity_lower:
            return "Italians"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "serbs" in ethnicity_lower:
            return "Serbs"
    # Cuba patterns
    elif country_name == "Cuba":
        if "afro-cubans" in ethnicity_lower:
            return "Afro-Cubans"
        if "whites" in ethnicity_lower:
            return "Whites"
    # Cyprus patterns
    elif country_name == "Cyprus":
        if "greek" in ethnicity_lower:
            return "Greeks"
        if "turks" in ethnicity_lower:
            return "Turks"
    # Czech Republic patterns
    elif country_name == "Czech Republic":
        if "czechs" in ethnicity_lower:
            return "Czechs"
    # Denmark patterns
    elif country_name == "Denmark":
        if "danes" in ethnicity_lower:
            return "Danes"
    # Djibouti patterns
    elif country_name == "Djibouti":
        if "afar" in ethnicity_lower:
            return "Afar"
        if "isaas" in ethnicity_lower:
            return "Isaas"
    # Dominican Republic patterns
    elif country_name == "Dominican Republic":
        if "dominicans" in ethnicity_lower:
            return "Dominicans"
    # East Timor patterns
    elif country_name == "East Timor":
        if "east timorese" in ethnicity_lower:
            return "East Timorese"
    # Ecuador patterns
    elif country_name == "Ecuador":
        if "afro-ecuadorians" in ethnicity_lower:
            return "Afro-Ecuadorians"
        if "indigenous highland peoples" in ethnicity_lower:
            return "Indigenous highland peoples"
        if "indigenous lowland peoples" in ethnicity_lower:
            return "Indigenous lowland peoples"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Egypt patterns
    elif country_name == "Egypt":
        if "arab muslims" in ethnicity_lower:
            return "Arab Muslims"
        if "coptic christians" in ethnicity_lower:
            return "Coptic Christians"
    # El Salvador patterns
    elif country_name == "El Salvador":
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Equatorial Guinea patterns
    elif country_name == "Equatorial Guinea":
        if "annobon islanders" in ethnicity_lower:
            return "Annobon Islanders"
        if "bubi" in ethnicity_lower:
            return "Bubi"
        if "fang" in ethnicity_lower:
            return "Fang"
        if "fernandinos" in ethnicity_lower:
            return "Fernandinos"
        if "ndowe" in ethnicity_lower:
            return "Ndowe"
    # Eritrea patterns
    elif country_name == "Eritrea":
        if "afar" in ethnicity_lower:
            return "Afar"
        if "christians" in ethnicity_lower:
            return "Christians"
        if "kunama" in ethnicity_lower:
            return "Kunama"
        if "other muslims" in ethnicity_lower:
            return "Other Muslims"
        if "saho" in ethnicity_lower:
            return "Saho"
    # Estonia patterns
    elif country_name == "Estonia":
        if "byelorussians" in ethnicity_lower:
            return "Byelorussians"
        if "estonians" in ethnicity_lower:
            return "Estonians"
        if "russians" in ethnicity_lower:
            return "Russians"
        if "ukrainians" in ethnicity_lower:
            return "Ukrainians"
    # Fiji patterns
    elif country_name == "Fiji":
        if "fijian" in ethnicity_lower:
            return "Fijians"
        if "indians" in ethnicity_lower:
            return "Indians"
    # Finland patterns
    elif country_name == "Finland":
        if "finns" in ethnicity_lower:
            return "Finns"
        if "swedes" in ethnicity_lower:
            return "Swedes"
    # France patterns
    elif country_name == "France":
        if "basques" in ethnicity_lower:
            return "Basques"
        if "corsicans" in ethnicity_lower:
            return "Corsicans"
        if "french" in ethnicity_lower:
            return "French"
        if "roma" in ethnicity_lower:
            return "Roma"
    # Gabon patterns
    elif country_name == "Gabon":
        if "eshira/bapounou" in ethnicity_lower:
            return "Eshira/Bapounou"
        if "fang" in ethnicity_lower:
            return "Fang"
        if "mbede" in ethnicity_lower:
            return "Mbede"
        if "myene" in ethnicity_lower:
            return "Myene"
    # Gambia patterns
    elif country_name == "Gambia":
        if "aku" in ethnicity_lower:
            return "Aku"
        if "diola" in ethnicity_lower:
            return "Diola"
        if "fula" in ethnicity_lower:
            return "Fula"
        if "mandinka" in ethnicity_lower:
            return "Mandinka"
        if "wolof" in ethnicity_lower:
            return "Wolof"
    # Georgia patterns
    elif country_name == "Georgia":
        if "abkhazians" in ethnicity_lower:
            return "Abkhazians"
        if "armenian" in ethnicity_lower:
            return "Armenians"
        if "azeri" in ethnicity_lower:
            return "Azeri"
        if "georgians" in ethnicity_lower:
            return "Georgians"
        if "ossetians" in ethnicity_lower:
            return "Ossetians"
    # German Federal Republic patterns
    elif country_name == "German Federal Republic":
        if "germans" in ethnicity_lower:
            return "Germans"
    # Ghana patterns
    elif country_name == "Ghana":
        if "asante" in ethnicity_lower:
            return "Asante"
        if "ewe" in ethnicity_lower:
            return "Ewe"
        if "ga-adangbe" in ethnicity_lower:
            return "Ga-Adangbe"
        if "northern groups" in ethnicity_lower:
            return "Northern Groups"
        if "other akans" in ethnicity_lower:
            return "Other Akans"
    # Greece patterns
    elif country_name == "Greece":
        if "greek" in ethnicity_lower:
            return "Greeks"
        if "macedonian" in ethnicity_lower:
            return "Macedonians"
        if "muslims" in ethnicity_lower:
            return "Muslims"
        if "roma" in ethnicity_lower:
            return "Roma"
    # Guatemala patterns
    elif country_name == "Guatemala":
        if "garífuna" in ethnicity_lower:
            return "Garífuna"
        if "ladinos" in ethnicity_lower:
            return "Ladinos"
        if "maya" in ethnicity_lower:
            return "Maya"
        if "xinca" in ethnicity_lower:
            return "Xinca"
    # Guinea patterns
    elif country_name == "Guinea":
        if "malinke" in ethnicity_lower:
            return "Malinke"
        if "peul" in ethnicity_lower:
            return "Peul"
        if "susu" in ethnicity_lower:
            return "Susu"
    # Guinea-Bissau patterns
    elif country_name == "Guinea-Bissau":
        if "balanta" in ethnicity_lower:
            return "Balanta"
        if "cape verdean" in ethnicity_lower:
            return "Cape Verdean"
        if "manjaco" in ethnicity_lower:
            return "Manjaco"
        if "papel" in ethnicity_lower:
            return "Papel"
    # Guyana patterns
    elif country_name == "Guyana":
        if "afro-guyanese" in ethnicity_lower:
            return "Afro-Guyanese"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "indo-guyanese" in ethnicity_lower:
            return "Indo-Guyanese"
    # Haiti patterns
    elif country_name == "Haiti":
        if "haitians" in ethnicity_lower:
            return "Haitians"
    # Honduras patterns
    elif country_name == "Honduras":
        if "garifuna" in ethnicity_lower:
            return "Garifuna"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Hungary patterns
    elif country_name == "Hungary":
        if "hungarian" in ethnicity_lower:
            return "Hungarians"
        if "roma" in ethnicity_lower:
            return "Roma"
    # Iceland patterns
    elif country_name == "Iceland":
        if "icelanders" in ethnicity_lower:
            return "Icelanders"
    # Iraq patterns
    elif country_name == "Iraq":
        if "assyrians" in ethnicity_lower:
            return "Assyrians"
        if "kurds" in ethnicity_lower:
            return "Kurds"
        if "shi'a arabs" in ethnicity_lower:
            return "Shi'a Arabs"
        if "sunni arabs" in ethnicity_lower:
            return "Sunni Arabs"
        if "turkmen" in ethnicity_lower:
            return "Turkmen"
    # Ireland patterns
    elif country_name == "Ireland":
        if "irish" in ethnicity_lower:
            return "Irish"
    # Israel patterns
    elif country_name == "Israel":
        if "ashkenazim" in ethnicity_lower:
            return "Ashkenazim"
        if "israeli arabs" in ethnicity_lower:
            return "Israeli Arabs"
        if "mizrahim" in ethnicity_lower:
            return "Mizrahim"
        if "palestinian arabs" in ethnicity_lower:
            return "Palestinian Arabs"
        if "russians" in ethnicity_lower:
            return "Russians"
    # Italy/Sardinia patterns
    elif country_name == "Italy/Sardinia":
        if "aostans" in ethnicity_lower:
            return "Aostans"
        if "friulians" in ethnicity_lower:
            return "Friulians"
        if "german speakers" in ethnicity_lower:
            return "German speakers"
        if "italians" in ethnicity_lower:
            return "Italians"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "sardinians" in ethnicity_lower:
            return "Sardinians"
    # Jamaica patterns
    elif country_name == "Jamaica":
        if "jamaicans" in ethnicity_lower:
            return "Jamaicans"
    # Japan patterns
    elif country_name == "Japan":
        if "ainu" in ethnicity_lower:
            return "Ainu"
        if "burakumin" in ethnicity_lower:
            return "Burakumin"
        if "japanese" in ethnicity_lower:
            return "Japanese"
        if "koreans" in ethnicity_lower:
            return "Koreans"
        if "okinawans" in ethnicity_lower:
            return "Okinawans"
    # Jordan patterns
    elif country_name == "Jordan":
        if "christians" in ethnicity_lower:
            return "Christians"
        if "jordanian arabs" in ethnicity_lower:
            return "Jordanian Arabs"
        if "palestinian arabs" in ethnicity_lower:
            return "Palestinian Arabs"
    # Kazakhstan patterns
    elif country_name == "Kazakhstan":
        if "germans" in ethnicity_lower:
            return "Germans"
        if "kazakhs" in ethnicity_lower:
            return "Kazakhs"
        if "russian-speakers" in ethnicity_lower:
            return "Russian-speakers"
        if "tatars" in ethnicity_lower:
            return "Tatars"
        if "uighur" in ethnicity_lower:
            return "Uighur"
        if "uzbeks" in ethnicity_lower:
            return "Uzbeks"
    # Korea, People's Republic of patterns
    elif country_name == "Korea, People's Republic of":
        if "koreans" in ethnicity_lower:
            return "Koreans"
    # Korea, Republic of patterns
    elif country_name == "Korea, Republic of":
        if "koreans" in ethnicity_lower:
            return "Koreans"
    # Kosovo patterns
    elif country_name == "Kosovo":
        if "albanian" in ethnicity_lower:
            return "Albanians"
        if "bosniaks" in ethnicity_lower:
            return "Bosniaks"
        if "gorani" in ethnicity_lower:
            return "Gorani"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "serbs" in ethnicity_lower:
            return "Serbs"
        if "turks" in ethnicity_lower:
            return "Turks"
    # Kuwait patterns
    elif country_name == "Kuwait":
        if "bedoon" in ethnicity_lower:
            return "Bedoon"
        if "kuwaiti shi'a" in ethnicity_lower:
            return "Kuwaiti Shi'a"
        if "kuwaiti sunni" in ethnicity_lower:
            return "Kuwaiti Sunni"
    # Kyrgyz Republic patterns
    elif country_name == "Kyrgyz Republic":
        if "kyrgyz" in ethnicity_lower:
            return "Kyrgyz"
        if "russians" in ethnicity_lower:
            return "Russians"
        if "uyghur" in ethnicity_lower:
            return "Uyghur"
        if "uzbeks" in ethnicity_lower:
            return "Uzbeks"
    # Laos patterns
    elif country_name == "Laos":
        if "hmong" in ethnicity_lower:
            return "Hmong"
        if "khmou" in ethnicity_lower:
            return "Khmou"
        if "lao" in ethnicity_lower:
            return "Lao"
        if "lao sung" in ethnicity_lower:
            return "Lao Sung"
        if "lao tai" in ethnicity_lower:
            return "Lao Tai"
        if "lao thoeng" in ethnicity_lower:
            return "Lao Thoeng"
    # Latvia patterns
    elif country_name == "Latvia":
        if "byelorussians" in ethnicity_lower:
            return "Byelorussians"
        if "latvians" in ethnicity_lower:
            return "Latvians"
        if "russians" in ethnicity_lower:
            return "Russians"
        if "ukrainians" in ethnicity_lower:
            return "Ukrainians"
    # Lesotho patterns
    elif country_name == "Lesotho":
        if "sotho" in ethnicity_lower:
            return "Sotho"
    # Liberia patterns
    elif country_name == "Liberia":
        if "americo-liberians" in ethnicity_lower:
            return "Americo-Liberians"
        if "gio" in ethnicity_lower:
            return "Gio"
        if "krahn" in ethnicity_lower:
            return "Krahn"
        if "kru" in ethnicity_lower:
            return "Kru"
        if "mandingo" in ethnicity_lower:
            return "Mandingo"
        if "mano" in ethnicity_lower:
            return "Mano"
    # Libya patterns
    elif country_name == "Libya":
        if "arab" in ethnicity_lower:
            return "Arabs"
        if "berber" in ethnicity_lower:
            return "Berbers"
        if "toubou" in ethnicity_lower:
            return "Toubou"
        if "tuareg" in ethnicity_lower:
            return "Tuareg"
    # Lithuania patterns
    elif country_name == "Lithuania":
        if "lithuanians" in ethnicity_lower:
            return "Lithuanians"
        if "poles" in ethnicity_lower:
            return "Poles"
        if "russians" in ethnicity_lower:
            return "Russians"
    # Luxembourg patterns
    elif country_name == "Luxembourg":
        if "luxembourger" in ethnicity_lower:
            return "Luxembourgers"
    # Madagascar (Malagasy) patterns
    elif country_name == "Madagascar (Malagasy)":
        if "côtiers" in ethnicity_lower:
            return "Côtiers"
        if "highlanders" in ethnicity_lower:
            return "Highlanders"
    # Malawi patterns
    elif country_name == "Malawi":
        if "central" in ethnicity_lower:
            return "Central"
        if "northerners" in ethnicity_lower:
            return "Northerners"
        if "southerners" in ethnicity_lower:
            return "Southerners"
    # Malaysia patterns
    elif country_name == "Malaysia":
        if "chinese" in ethnicity_lower:
            return "Chinese"
        if "dayaks" in ethnicity_lower:
            return "Dayaks"
        if "east indians" in ethnicity_lower:
            return "East Indians"
        if "kadazans" in ethnicity_lower:
            return "Kadazans"
        if "malays" in ethnicity_lower:
            return "Malays"
        if "orang asli" in ethnicity_lower:
            return "Orang Asli"
    # Maldives patterns
    elif country_name == "Maldives":
        if "divehis" in ethnicity_lower:
            return "Divehis"
    # Mali patterns
    elif country_name == "Mali":
        if "arabs/moors" in ethnicity_lower:
            return "Arabs/Moors"
        if "blacks" in ethnicity_lower:
            return "Blacks"
        if "tuareg" in ethnicity_lower:
            return "Tuareg"
    # Malta patterns
    elif country_name == "Malta":
        if "maltese" in ethnicity_lower:
            return "Maltese"
    # Mauritania patterns
    elif country_name == "Mauritania":
        if "black africans" in ethnicity_lower:
            return "Black Africans"
        if "haratins" in ethnicity_lower:
            return "Haratins"
        if "white moors" in ethnicity_lower:
            return "White Moors"
    # Mexico patterns
    elif country_name == "Mexico":
        if "afromexicans" in ethnicity_lower:
            return "Afromexicans"
        if "maya" in ethnicity_lower:
            return "Maya"
        if "mestizos" in ethnicity_lower:
            return "Mestizos"
        if "other indigenous groups" in ethnicity_lower:
            return "Other indigenous groups"
    # Moldova patterns
    elif country_name == "Moldova":
        if "bulgarians" in ethnicity_lower:
            return "Bulgarians"
        if "gagauz" in ethnicity_lower:
            return "Gagauz"
        if "moldovans" in ethnicity_lower:
            return "Moldovans"
        if "russian speakers" in ethnicity_lower:
            return "Russian speakers"
    # Mongolia patterns
    elif country_name == "Mongolia":
        if "kazakh" in ethnicity_lower:
            return "Kazakh"
        if "mongols" in ethnicity_lower:
            return "Mongols"
    # Montenegro patterns
    elif country_name == "Montenegro":
        if "albanian" in ethnicity_lower:
            return "Albanians"
        if "bosniak/muslims" in ethnicity_lower:
            return "Bosniak/Muslims"
        if "croats" in ethnicity_lower:
            return "Croats"
        if "montenegrins" in ethnicity_lower:
            return "Montenegrins"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "serbs" in ethnicity_lower:
            return "Serbs"
    # Morocco patterns
    elif country_name == "Morocco":
        if "arab" in ethnicity_lower:
            return "Arabs"
        if "berber" in ethnicity_lower:
            return "Berbers"
        if "sahrawis" in ethnicity_lower:
            return "Sahrawis"
    # Mozambique patterns
    elif country_name == "Mozambique":
        if "makonde-yao" in ethnicity_lower:
            return "Makonde-Yao"
        if "shona-ndau" in ethnicity_lower:
            return "Shona-Ndau"
        if "tsonga-chopi" in ethnicity_lower:
            return "Tsonga-Chopi"
    # Nepal patterns
    elif country_name == "Nepal":
        if "adibasi janajati" in ethnicity_lower:
            return "Adibasi Janajati"
        if "caste hill hindu elite" in ethnicity_lower:
            return "Caste Hill Hindu Elite"
        if "dalits" in ethnicity_lower:
            return "Dalits"
        if "madhesi" in ethnicity_lower:
            return "Madhesi"
        if "muslims" in ethnicity_lower:
            return "Muslims"
        if "newars" in ethnicity_lower:
            return "Newars"
    # Netherlands patterns
    elif country_name == "Netherlands":
        if "dutch" in ethnicity_lower:
            return "Dutch"
    # New Zealand patterns
    elif country_name == "New Zealand":
        if "asians" in ethnicity_lower:
            return "Asians"
        if "maori" in ethnicity_lower:
            return "Maori"
        if "new zealanders" in ethnicity_lower:
            return "New Zealanders"
        if "pacific islanders" in ethnicity_lower:
            return "Pacific Islanders"
    # Nicaragua patterns
    elif country_name == "Nicaragua":
        if "afronicaraguans" in ethnicity_lower:
            return "Afronicaraguans"
        if "miskitos" in ethnicity_lower:
            return "Miskitos"
        if "sumus" in ethnicity_lower:
            return "Sumus"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Niger patterns
    elif country_name == "Niger":
        if "djerma-songhai" in ethnicity_lower:
            return "Djerma-Songhai"
        if "hausa" in ethnicity_lower:
            return "Hausa"
        if "kanouri" in ethnicity_lower:
            return "Kanouri"
        if "toubou" in ethnicity_lower:
            return "Toubou"
        if "tuareg" in ethnicity_lower:
            return "Tuareg"
    # Nigeria patterns
    elif country_name == "Nigeria":
        if "hausa-fulani and muslim middle belt" in ethnicity_lower:
            return "Hausa-Fulani and Muslim Middle Belt"
        if "igbo" in ethnicity_lower:
            return "Igbo"
        if "ijaw" in ethnicity_lower:
            return "Ijaw"
        if "ogoni" in ethnicity_lower:
            return "Ogoni"
        if "tiv" in ethnicity_lower:
            return "Tiv"
        if "yoruba" in ethnicity_lower:
            return "Yoruba"
    # Norway patterns
    elif country_name == "Norway":
        if "norwegians" in ethnicity_lower:
            return "Norwegians"
    # Oman patterns
    elif country_name == "Oman":
        if "ibadhi muslims" in ethnicity_lower:
            return "Ibadhi Muslims"
    # Panama patterns
    elif country_name == "Panama":
        if "afropanamanians" in ethnicity_lower:
            return "Afropanamanians"
        if "choco" in ethnicity_lower:
            return "Choco"
        if "kuna" in ethnicity_lower:
            return "Kuna"
        if "ngäbe-buglé" in ethnicity_lower:
            return "Ngäbe-Buglé"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Papua New Guinea patterns
    elif country_name == "Papua New Guinea":
        if "bougainvilleans" in ethnicity_lower:
            return "Bougainvilleans"
        if "papua new guineans" in ethnicity_lower:
            return "Papua New Guineans"
    # Paraguay patterns
    elif country_name == "Paraguay":
        if "tupi-guaraní and other indigenous groups" in ethnicity_lower:
            return "Tupi-Guaraní and other indigenous groups"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Peru patterns
    elif country_name == "Peru":
        if "afroperuvians" in ethnicity_lower:
            return "Afroperuvians"
        if "indigenous peoples of the amazon" in ethnicity_lower:
            return "Indigenous peoples of the Amazon"
        if "indigenous peoples of the andes" in ethnicity_lower:
            return "Indigenous peoples of the Andes"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Philippines patterns
    elif country_name == "Philippines":
        if "christian lowlanders" in ethnicity_lower:
            return "Christian lowlanders"
        if "fil-chinese" in ethnicity_lower:
            return "Fil-Chinese"
        if "indigenous" in ethnicity_lower:
            return "Indigenous"
        if "moro" in ethnicity_lower:
            return "Moro"
    # Poland patterns
    elif country_name == "Poland":
        if "byelorussians" in ethnicity_lower:
            return "Byelorussians"
        if "european and american jews" in ethnicity_lower:
            return "European and American Jews"
        if "germans" in ethnicity_lower:
            return "Germans"
        if "poles" in ethnicity_lower:
            return "Poles"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "ukrainians" in ethnicity_lower:
            return "Ukrainians"
    # Portugal patterns
    elif country_name == "Portugal":
        if "portuguese" in ethnicity_lower:
            return "Portuguese"
    # Qatar patterns
    elif country_name == "Qatar":
        if "qatari arabs" in ethnicity_lower:
            return "Qatari Arabs"
    # Rumania patterns
    elif country_name == "Rumania":
        if "germans" in ethnicity_lower:
            return "Germans"
        if "hungarian" in ethnicity_lower:
            return "Hungarians"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "romanians" in ethnicity_lower:
            return "Romanians"
    # Rwanda patterns
    elif country_name == "Rwanda":
        if "hutu" in ethnicity_lower:
            return "Hutu"
        if "tutsi" in ethnicity_lower:
            return "Tutsi"
    # Saudi Arabia patterns
    elif country_name == "Saudi Arabia":
        if "ismaili shia" in ethnicity_lower:
            return "Ismaili Shia"
        if "ja'afari shia" in ethnicity_lower:
            return "Ja'afari Shia"
        if "sunni shafii/sofi" in ethnicity_lower:
            return "Sunni Shafii/Sofi"
        if "sunni wahhabi" in ethnicity_lower:
            return "Sunni Wahhabi"
    # Senegal patterns
    elif country_name == "Senegal":
        if "diola" in ethnicity_lower:
            return "Diola"
        if "mandingue" in ethnicity_lower:
            return "Mandingue"
        if "pulaar" in ethnicity_lower:
            return "Pulaar"
        if "serer" in ethnicity_lower:
            return "Serer"
        if "wolof" in ethnicity_lower:
            return "Wolof"
    # Sierra Leone patterns
    elif country_name == "Sierra Leone":
        if "creole" in ethnicity_lower:
            return "Creole"
        if "kono" in ethnicity_lower:
            return "Kono"
        if "limba" in ethnicity_lower:
            return "Limba"
        if "mende" in ethnicity_lower:
            return "Mende"
        if "temne" in ethnicity_lower:
            return "Temne"
    # Singapore patterns
    elif country_name == "Singapore":
        if "chinese" in ethnicity_lower:
            return "Chinese"
        if "eurasians and others" in ethnicity_lower:
            return "Eurasians and Others"
        if "indians" in ethnicity_lower:
            return "Indians"
        if "malays" in ethnicity_lower:
            return "Malays"
    # Slovakia patterns
    elif country_name == "Slovakia":
        if "hungarian" in ethnicity_lower:
            return "Hungarians"
        if "slovaks" in ethnicity_lower:
            return "Slovaks"
    # Slovenia patterns
    elif country_name == "Slovenia":
        if "hungarian" in ethnicity_lower:
            return "Hungarians"
        if "italians" in ethnicity_lower:
            return "Italians"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "slovenes" in ethnicity_lower:
            return "Slovenes"
    # Solomon Islands patterns
    elif country_name == "Solomon Islands":
        if "solomon islanders" in ethnicity_lower:
            return "Solomon Islanders"
    # Somalia patterns
    elif country_name == "Somalia":
        if "somali" in ethnicity_lower:
            return "Somali"
    # Spain patterns
    elif country_name == "Spain":
        if "basques" in ethnicity_lower:
            return "Basques"
        if "catalans" in ethnicity_lower:
            return "Catalans"
        if "galicians" in ethnicity_lower:
            return "Galicians"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "spanish" in ethnicity_lower:
            return "Spanish"
    # Sri Lanka (Ceylon) patterns
    elif country_name == "Sri Lanka (Ceylon)":
        if "indian tamils" in ethnicity_lower:
            return "Indian Tamils"
        if "moors" in ethnicity_lower:
            return "Moors"
        if "sinhalese" in ethnicity_lower:
            return "Sinhalese"
        if "sri lankan tamils" in ethnicity_lower:
            return "Sri Lankan Tamils"
    # Surinam patterns
    elif country_name == "Surinam":
        if "chinese" in ethnicity_lower:
            return "Chinese"
        if "creoles" in ethnicity_lower:
            return "Creoles"
        if "east indians" in ethnicity_lower:
            return "East Indians"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous Peoples"
        if "javanese" in ethnicity_lower:
            return "Javanese"
        if "maroons" in ethnicity_lower:
            return "Maroons"
    # Swaziland (Eswatini) patterns
    elif country_name == "Swaziland (Eswatini)":
        if "swazi" in ethnicity_lower:
            return "Swazi"
    # Sweden patterns
    elif country_name == "Sweden":
        if "swedes" in ethnicity_lower:
            return "Swedes"
    # Switzerland patterns
    elif country_name == "Switzerland":
        if "swiss french" in ethnicity_lower:
            return "Swiss French"
        if "swiss germans" in ethnicity_lower:
            return "Swiss Germans"
        if "swiss italians" in ethnicity_lower:
            return "Swiss Italians"
    # Syria patterns
    elif country_name == "Syria":
        if "alawi" in ethnicity_lower:
            return "Alawi"
        if "christians" in ethnicity_lower:
            return "Christians"
        if "druze" in ethnicity_lower:
            return "Druze"
        if "kurds" in ethnicity_lower:
            return "Kurds"
        if "sunni arabs" in ethnicity_lower:
            return "Sunni Arabs"
    # Taiwan patterns
    elif country_name == "Taiwan":
        if "indigenous/aboriginal taiwanese" in ethnicity_lower:
            return "Indigenous/Aboriginal Taiwanese"
        if "mainland chinese" in ethnicity_lower:
            return "Mainland Chinese"
        if "taiwanese" in ethnicity_lower:
            return "Taiwanese"
    # Tajikistan patterns
    elif country_name == "Tajikistan":
        if "kyrgyz" in ethnicity_lower:
            return "Kyrgyz"
        if "pamiri tajiks" in ethnicity_lower:
            return "Pamiri Tajiks"
        if "russians" in ethnicity_lower:
            return "Russians"
        if "tajiks" in ethnicity_lower:
            return "Tajiks"
        if "tatars" in ethnicity_lower:
            return "Tatars"
        if "uzbeks" in ethnicity_lower:
            return "Uzbeks"
    # Tanzania (Tanganyika) patterns
    elif country_name == "Tanzania (Tanganyika)":
        if "maasai" in ethnicity_lower:
            return "Maasai"
        if "mainland muslims" in ethnicity_lower:
            return "Mainland Muslims"
        if "others mainland" in ethnicity_lower:
            return "Others Mainland"
        if "shirazi" in ethnicity_lower:
            return "Shirazi"
        if "zanzibar arabs" in ethnicity_lower:
            return "Zanzibar Arabs"
    # Thailand patterns
    elif country_name == "Thailand":
        if "chinese" in ethnicity_lower:
            return "Chinese"
        if "hill tribes" in ethnicity_lower:
            return "Hill Tribes"
        if "malay muslims" in ethnicity_lower:
            return "Malay Muslims"
        if "shan" in ethnicity_lower:
            return "Shan"
        if "thai" in ethnicity_lower:
            return "Thai"
    # Togo patterns
    elif country_name == "Togo":
        if "ewe" in ethnicity_lower:
            return "Ewe"
        if "kabré" in ethnicity_lower:
            return "Kabré"
    # Trinidad and Tobago patterns
    elif country_name == "Trinidad and Tobago":
        if "blacks" in ethnicity_lower:
            return "Blacks"
        if "east indians" in ethnicity_lower:
            return "East Indians"
    # Tunisia patterns
    elif country_name == "Tunisia":
        if "arab" in ethnicity_lower:
            return "Arabs"
    # Turkey (Ottoman Empire) patterns
    elif country_name == "Turkey (Ottoman Empire)":
        if "kurds" in ethnicity_lower:
            return "Kurds"
        if "roma" in ethnicity_lower:
            return "Roma"
        if "turkish" in ethnicity_lower:
            return "Turkish"
    # Turkmenistan patterns
    elif country_name == "Turkmenistan":
        if "kazakhs" in ethnicity_lower:
            return "Kazakhs"
        if "russians" in ethnicity_lower:
            return "Russians"
        if "turkmen" in ethnicity_lower:
            return "Turkmen"
        if "uzbeks" in ethnicity_lower:
            return "Uzbeks"
    # Ukraine patterns
    elif country_name == "Ukraine":
        if "crimean tatars" in ethnicity_lower:
            return "Crimean Tatars"
        if "hungarian" in ethnicity_lower:
            return "Hungarians"
        if "romanians/moldovans" in ethnicity_lower:
            return "Romanians/Moldovans"
        if "russians" in ethnicity_lower:
            return "Russians"
        if "rusyns" in ethnicity_lower:
            return "Rusyns"
        if "ukrainians" in ethnicity_lower:
            return "Ukrainians"
    # United Arab Emirates patterns
    elif country_name == "United Arab Emirates":
        if "emirati arabs" in ethnicity_lower:
            return "Emirati Arabs"
    # United Kingdom patterns
    elif country_name == "United Kingdom":
        if "afro-caribbeans" in ethnicity_lower:
            return "Afro-Caribbeans"
        if "asians" in ethnicity_lower:
            return "Asians"
        if "catholics in n. ireland" in ethnicity_lower:
            return "Catholics In N. Ireland"
        if "english" in ethnicity_lower:
            return "English"
        if "protestants in n. ireland" in ethnicity_lower:
            return "Protestants In N. Ireland"
        if "scots" in ethnicity_lower:
            return "Scots"
        if "welsh" in ethnicity_lower:
            return "Welsh"
    # United States of America patterns
    elif country_name == "United States of America":
        if "african americans" in ethnicity_lower:
            return "African Americans"
        if "american indians" in ethnicity_lower:
            return "American Indians"
        if "arab americans" in ethnicity_lower:
            return "Arab Americans"
        if "asian americans" in ethnicity_lower:
            return "Asian Americans"
        if "latinos" in ethnicity_lower:
            return "Latinos"
        if "whites" in ethnicity_lower:
            return "Whites"
    # Uruguay patterns
    elif country_name == "Uruguay":
        if "afro-uruguayans" in ethnicity_lower:
            return "Afro-Uruguayans"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Uzbekistan patterns
    elif country_name == "Uzbekistan":
        if "karakalpak" in ethnicity_lower:
            return "Karakalpak"
        if "russians" in ethnicity_lower:
            return "Russians"
        if "tajiks" in ethnicity_lower:
            return "Tajiks"
        if "uzbeks" in ethnicity_lower:
            return "Uzbeks"
    # Venezuela patterns
    elif country_name == "Venezuela":
        if "afrovenezuelans" in ethnicity_lower:
            return "Afrovenezuelans"
        if "indigenous peoples" in ethnicity_lower:
            return "Indigenous peoples"
        if "whites/mestizos" in ethnicity_lower:
            return "Whites/mestizos"
    # Yemen (Arab Republic of Yemen) patterns
    elif country_name == "Yemen (Arab Republic of Yemen)":
        if "al-akhdam" in ethnicity_lower:
            return "Al-Akhdam"
        if "northern shafi'i" in ethnicity_lower:
            return "Northern Shafi'i"
        if "northern zaydis" in ethnicity_lower:
            return "Northern Zaydis"
        if "southern shafi'i" in ethnicity_lower:
            return "Southern Shafi'i"
    # Zimbabwe (Rhodesia) patterns
    elif country_name == "Zimbabwe (Rhodesia)":
        if "ndebele-kalanga-" in ethnicity_lower:
            return "Ndebele-Kalanga-"
        if "shona" in ethnicity_lower:
            return "Shona"
        if "white zimbabweans" in ethnicity_lower:
            return "White Zimbabweans"

    # Return original if no pattern matches
    return ethnicity


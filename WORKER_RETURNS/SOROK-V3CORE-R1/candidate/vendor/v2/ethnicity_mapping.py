# Ethnicity name mapping: people_groups → EPR-2021
# Auto-generated with improved pattern matching
# Used by get_epr_power_status() to match ethnicity names
# Format: people_groups name → EPR group name
#
# Strategy:
# 1. Exact matches (mapping dictionary)
# 2. Pattern matches (Java * → Javanese, Batak * → Bataks, etc.)
# 3. This gives granular ethnicity from JP + power status from EPR

ETHNICITY_NAME_MAPPING = {
    "Acehnese": "Acehnese",
    "Ambonese": "Amboinese",
    "Balinese": "Balinese",
    "Batak Angkola": "Bataks",
    "Batak Dairi": "Bataks",
    "Batak Karo": "Bataks",
    "Batak Pakpak": "Bataks",
    "Batak Simalungun": "Bataks",
    "Batak, Silindung": "Bataks",
    "Batak, Toba": "Bataks",
    "Daya": "Dayak",
    "Dayak": "Dayak",
    "Gorontalo": "Gorontalos",
    "Java Banten": "Javanese",
    "Java Banyumasan": "Javanese",
    "Java Mancanegari": "Javanese",
    "Java Negarigung": "Javanese",
    "Java Pesisir Kulon": "Javanese",
    "Java Pesisir Lor": "Javanese",
    "Java Serang": "Javanese",
    "Javanese": "Javanese",
    "Madura": "Madura",
    "Madurese": "Madura",
    "Makassar": "Makassarese and Bugis",
    "Malay, Bacanese": "Malay",
    "Malay, Banda": "Malay",
    "Malay, Ketapang": "Malay",
    "Malay, Larantuka": "Malay",
    "Malay, North Moluccan": "Malay",
    "Malay, Pontianak": "Malay",
    "Malay, Riau": "Malay",
    "Malay, Sambas": "Malay",
    "Malay, Singkil": "Malay",
    "Malay, Sumatera North": "Malay",
    "Minangkabau": "Minangkabaus",
    "Sunda": "Sundanese",
    "Ternate": "Ternate",
    "Timorese": "East Timorese",
}

# GroupID to EPR name mapping (fallback when name doesn't match)
GROUPID_TO_EPR = {
    "Acehnese": "1000",
    "Amboinese": "2000",
    "Balinese": "3000",
    "Bataks": "4000",
    "Chinese (Han)": "5000",
    "Dayak": "16000",
    "East Timorese": "6000",
    "Gorontalos": "7000",
    "Javanese": "8000",
    "Madura": "9000",
    "Makassarese and Bugis": "10000",
    "Malay": "17000",
    "Minahasa": "11000",
    "Minangkabaus": "12000",
    "Papuans": "13000",
    "Sundanese": "14000",
    "Ternate": "15000",
}

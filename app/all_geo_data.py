"""
TerraLux AI — Référentiel SIG Complet (Luxembourg & Madagascar - Diana)
Contient :
1. Luxembourg : 2 régions (Oesling, Gutland), 12 cantons, 100+ communes (avec les 12 villes officielles), et localités avec lat/lon
2. Madagascar (Diana) : Région Diana, 5 cantons/districts (Antsiranana I, Antsiranana II, Ambanja, Ambilobe, Nosy Be),
   toutes les communes et localités avec lat/lon
"""

GEO_REGIONS = [
    {
        "name": "Oesling",
        "country": "LUX",
        "description": "Plateau ardennais septentrional du Luxembourg (400-560m). Climat rude et frais, sols schisto-quartziteux (Cambisols dystriques).",
        "typical_ph": 5.9,
        "soil_type": "Sols schisteux et quartziteux ardennais (Cambisols dystriques)"
    },
    {
        "name": "Gutland",
        "country": "LUX",
        "description": "Région centre et sud du Luxembourg (130-350m). Climat tempéré, sols marno-calcaires et alluviaux (Cambisols calcaro-eutriques, Luvisols).",
        "typical_ph": 6.7,
        "soil_type": "Sols marno-calcaires et alluviaux fertiles (Cambisols calcaro-eutriques / Luvisols)"
    },
    {
        "name": "Diana",
        "country": "MDG",
        "description": "Région septentrionale de Madagascar (Antsiranana, Ambanja, Ambilobe, Nosy Be). Climat tropical chaud et humide, sols Ferralsols et Vertisols.",
        "typical_ph": 5.8,
        "soil_type": "Ferralsols rhodi-lixiques tropicaux et Vertisols alluviaux"
    }
]

GEO_CANTONS = [
    # Luxembourg - Oesling
    {"name": "Clervaux", "region": "Oesling", "country": "LUX"},
    {"name": "Wiltz", "region": "Oesling", "country": "LUX"},
    {"name": "Vianden", "region": "Oesling", "country": "LUX"},

    # Luxembourg - Gutland
    {"name": "Capellen", "region": "Gutland", "country": "LUX"},
    {"name": "Diekirch", "region": "Gutland", "country": "LUX"},
    {"name": "Echternach", "region": "Gutland", "country": "LUX"},
    {"name": "Esch-sur-Alzette", "region": "Gutland", "country": "LUX"},
    {"name": "Grevenmacher", "region": "Gutland", "country": "LUX"},
    {"name": "Luxembourg", "region": "Gutland", "country": "LUX"},
    {"name": "Mersch", "region": "Gutland", "country": "LUX"},
    {"name": "Redange", "region": "Gutland", "country": "LUX"},
    {"name": "Remich", "region": "Gutland", "country": "LUX"},

    # Madagascar - Diana (Districts administratifs)
    {"name": "Antsiranana I", "region": "Diana", "country": "MDG"},
    {"name": "Antsiranana II", "region": "Diana", "country": "MDG"},
    {"name": "Ambanja", "region": "Diana", "country": "MDG"},
    {"name": "Ambilobe", "region": "Diana", "country": "MDG"},
    {"name": "Nosy Be", "region": "Diana", "country": "MDG"}
]

# Les 100+ communes du Luxembourg et communes de Diana
GEO_COMMUNES_AND_LOCALITIES = [
    # =========================================================================
    # LUXEMBOURG : CANTON DE CLERVAUX (Oesling)
    # =========================================================================
    {
        "commune": "Clervaux",
        "canton": "Clervaux",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Clervaux", "lat": 50.055, "lon": 6.030},
            {"name": "Eselborn", "lat": 49.996, "lon": 6.007},
            {"name": "Reuler", "lat": 50.057, "lon": 6.035},
            {"name": "Urspelt", "lat": 50.075, "lon": 6.046},
            {"name": "Munshausen", "lat": 50.033, "lon": 6.037},
            {"name": "Drauffelt", "lat": 50.016, "lon": 6.004},
            {"name": "Mecher", "lat": 50.027, "lon": 5.992},
            {"name": "Weicherdange", "lat": 50.039, "lon": 5.989}
        ]
    },
    {
        "commune": "Troisvierges",
        "canton": "Clervaux",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Troisvierges", "lat": 50.120, "lon": 5.990},
            {"name": "Wilwerdange", "lat": 50.138, "lon": 6.021},
            {"name": "Huldange", "lat": 50.165, "lon": 6.015},
            {"name": "Basbellain", "lat": 50.155, "lon": 5.975},
            {"name": "Hautbellain", "lat": 50.161, "lon": 5.955},
            {"name": "Drinklange", "lat": 50.141, "lon": 6.002},
            {"name": "Goedange", "lat": 50.145, "lon": 6.047}
        ]
    },
    {
        "commune": "Parc Hosingen",
        "canton": "Clervaux",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Hosingen", "lat": 50.012, "lon": 6.089},
            {"name": "Dorscheid", "lat": 50.028, "lon": 6.096},
            {"name": "Holzthum", "lat": 49.988, "lon": 6.067},
            {"name": "Consthum", "lat": 49.974, "lon": 6.054}
        ]
    },
    {
        "commune": "Weiswampach",
        "canton": "Clervaux",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Weiswampach", "lat": 50.138, "lon": 6.074},
            {"name": "Breidfeld", "lat": 50.127, "lon": 6.058},
            {"name": "Binsfeld", "lat": 50.118, "lon": 6.054}
        ]
    },
    {
        "commune": "Wincrange",
        "canton": "Clervaux",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Wincrange", "lat": 50.053, "lon": 5.918},
            {"name": "Asselborn", "lat": 50.096, "lon": 5.974},
            {"name": "Boevange", "lat": 50.061, "lon": 5.933},
            {"name": "Boxhorn", "lat": 50.082, "lon": 5.989}
        ]
    },

    # =========================================================================
    # LUXEMBOURG : CANTON DE WILTZ (Oesling)
    # =========================================================================
    {
        "commune": "Wiltz",
        "canton": "Wiltz",
        "country": "LUX",
        "is_city": True, # Ville officielle 1/12
        "localities": [
            {"name": "Wiltz", "lat": 49.967, "lon": 5.933},
            {"name": "Roullingen", "lat": 49.954, "lon": 5.925},
            {"name": "Weidingen", "lat": 49.962, "lon": 5.949},
            {"name": "Eschweiler", "lat": 49.998, "lon": 5.952},
            {"name": "Erpeldange-Wiltz", "lat": 49.979, "lon": 5.932}
        ]
    },
    {
        "commune": "Boulaide",
        "canton": "Wiltz",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Boulaide", "lat": 49.888, "lon": 5.815},
            {"name": "Baschleiden", "lat": 49.897, "lon": 5.845}
        ]
    },
    {
        "commune": "Esch-sur-Sûre",
        "canton": "Wiltz",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Esch-sur-Sûre", "lat": 49.911, "lon": 5.936},
            {"name": "Heiderscheid", "lat": 49.892, "lon": 5.986},
            {"name": "Eschdorf", "lat": 49.886, "lon": 5.934}
        ]
    },
    {
        "commune": "Goesdorf",
        "canton": "Wiltz",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Goesdorf", "lat": 49.921, "lon": 5.968},
            {"name": "Dahl", "lat": 49.932, "lon": 5.978}
        ]
    },
    {
        "commune": "Kiischpelt",
        "canton": "Wiltz",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Kiischpelt", "lat": 49.988, "lon": 6.002},
            {"name": "Kautenbach", "lat": 49.952, "lon": 6.021},
            {"name": "Wilwerwiltz", "lat": 49.989, "lon": 5.998}
        ]
    },
    {
        "commune": "Lac de la Haute-Sûre",
        "canton": "Wiltz",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Bavigne", "lat": 49.923, "lon": 5.852},
            {"name": "Kaundorf", "lat": 49.921, "lon": 5.903},
            {"name": "Mecher-Haute-Sûre", "lat": 49.926, "lon": 5.875}
        ]
    },
    {
        "commune": "Winseler",
        "canton": "Wiltz",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Winseler", "lat": 49.967, "lon": 5.890},
            {"name": "Doncols", "lat": 49.975, "lon": 5.834}
        ]
    },

    # =========================================================================
    # LUXEMBOURG : CANTON DE VIANDEN (Oesling)
    # =========================================================================
    {
        "commune": "Vianden",
        "canton": "Vianden",
        "country": "LUX",
        "is_city": True, # Ville officielle 2/12
        "localities": [
            {"name": "Vianden", "lat": 49.934, "lon": 6.209}
        ]
    },
    {
        "commune": "Putscheid",
        "canton": "Vianden",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Putscheid", "lat": 49.961, "lon": 6.143},
            {"name": "Stolzembourg", "lat": 49.970, "lon": 6.171}
        ]
    },
    {
        "commune": "Tandel",
        "canton": "Vianden",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Tandel", "lat": 49.897, "lon": 6.182},
            {"name": "Fouhren", "lat": 49.905, "lon": 6.200},
            {"name": "Bastendorf", "lat": 49.889, "lon": 6.167}
        ]
    },

    # =========================================================================
    # LUXEMBOURG : CANTON DE DIEKIRCH (Gutland)
    # =========================================================================
    {
        "commune": "Diekirch",
        "canton": "Diekirch",
        "country": "LUX",
        "is_city": True, # Ville officielle 3/12
        "localities": [
            {"name": "Diekirch", "lat": 49.868, "lon": 6.160}
        ]
    },
    {
        "commune": "Ettelbruck",
        "canton": "Diekirch",
        "country": "LUX",
        "is_city": True, # Ville officielle 4/12
        "localities": [
            {"name": "Ettelbruck", "lat": 49.847, "lon": 6.104},
            {"name": "Warken", "lat": 49.858, "lon": 6.096}
        ]
    },
    {
        "commune": "Bettendorf",
        "canton": "Diekirch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Bettendorf", "lat": 49.876, "lon": 6.218},
            {"name": "Gilsdorf", "lat": 49.864, "lon": 6.183}
        ]
    },
    {
        "commune": "Bourscheid",
        "canton": "Diekirch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Bourscheid", "lat": 49.909, "lon": 6.066},
            {"name": "Michelau", "lat": 49.900, "lon": 6.091}
        ]
    },
    {
        "commune": "Erpeldange-sur-Sûre",
        "canton": "Diekirch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Erpeldange-sur-Sûre", "lat": 49.861, "lon": 6.113},
            {"name": "Ingeldorf", "lat": 49.853, "lon": 6.141}
        ]
    },
    {
        "commune": "Feulen",
        "canton": "Diekirch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Niederfeulen", "lat": 49.854, "lon": 6.046},
            {"name": "Oberfeulen", "lat": 49.858, "lon": 6.030}
        ]
    },
    {
        "commune": "Mertzig",
        "canton": "Diekirch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Mertzig", "lat": 49.832, "lon": 6.002}
        ]
    },
    {
        "commune": "Reisdorf",
        "canton": "Diekirch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Reisdorf", "lat": 49.868, "lon": 6.269},
            {"name": "Wallendorf-Pont", "lat": 49.874, "lon": 6.290}
        ]
    },
    {
        "commune": "Schieren",
        "canton": "Diekirch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Schieren", "lat": 49.830, "lon": 6.096}
        ]
    },
    {
        "commune": "Vallée de l'Ernz",
        "canton": "Diekirch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Medernach", "lat": 49.809, "lon": 6.218},
            {"name": "Ermsdorf", "lat": 49.829, "lon": 6.220},
            {"name": "Stegen", "lat": 49.828, "lon": 6.177}
        ]
    },

    # =========================================================================
    # LUXEMBOURG : CANTON D'ECHTERNACH (Gutland)
    # =========================================================================
    {
        "commune": "Echternach",
        "canton": "Echternach",
        "country": "LUX",
        "is_city": True, # Ville officielle 5/12
        "localities": [
            {"name": "Echternach", "lat": 49.812, "lon": 6.421}
        ]
    },
    {
        "commune": "Beaufort",
        "canton": "Echternach",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Beaufort", "lat": 49.834, "lon": 6.291},
            {"name": "Dillingen", "lat": 49.854, "lon": 6.319}
        ]
    },
    {
        "commune": "Bech",
        "canton": "Echternach",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Bech", "lat": 49.753, "lon": 6.362},
            {"name": "Altrier", "lat": 49.751, "lon": 6.327}
        ]
    },
    {
        "commune": "Berdorf",
        "canton": "Echternach",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Berdorf", "lat": 49.821, "lon": 6.350},
            {"name": "Bollendorf-Pont", "lat": 49.851, "lon": 6.363}
        ]
    },
    {
        "commune": "Consdorf",
        "canton": "Echternach",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Consdorf", "lat": 49.779, "lon": 6.338},
            {"name": "Scheidgen", "lat": 49.782, "lon": 6.357}
        ]
    },
    {
        "commune": "Rosport-Mompach",
        "canton": "Echternach",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Rosport", "lat": 49.799, "lon": 6.502},
            {"name": "Mompach", "lat": 49.750, "lon": 6.467},
            {"name": "Born", "lat": 49.761, "lon": 6.516}
        ]
    },
    {
        "commune": "Waldbillig",
        "canton": "Echternach",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Waldbillig", "lat": 49.796, "lon": 6.287},
            {"name": "Christnach", "lat": 49.789, "lon": 6.270},
            {"name": "Mullerthal", "lat": 49.791, "lon": 6.305}
        ]
    },

    # =========================================================================
    # LUXEMBOURG : CANTON D'ESCH-SUR-ALZETTE (Gutland / Minett)
    # =========================================================================
    {
        "commune": "Esch-sur-Alzette",
        "canton": "Esch-sur-Alzette",
        "country": "LUX",
        "is_city": True, # Ville officielle 9/12
        "localities": [
            {"name": "Esch-sur-Alzette", "lat": 49.497, "lon": 5.981},
            {"name": "Belval", "lat": 49.502, "lon": 5.928},
            {"name": "Lallange", "lat": 49.510, "lon": 5.990},
            {"name": "Sommet", "lat": 49.490, "lon": 5.980}
        ]
    },
    {
        "commune": "Differdange",
        "canton": "Esch-sur-Alzette",
        "country": "LUX",
        "is_city": True, # Ville officielle 10/12
        "localities": [
            {"name": "Differdange", "lat": 49.524, "lon": 5.891},
            {"name": "Niederkorn", "lat": 49.537, "lon": 5.892},
            {"name": "Oberkorn", "lat": 49.514, "lon": 5.894},
            {"name": "Lasauvage", "lat": 49.513, "lon": 5.845}
        ]
    },
    {
        "commune": "Dudelange",
        "canton": "Esch-sur-Alzette",
        "country": "LUX",
        "is_city": True, # Ville officielle 11/12
        "localities": [
            {"name": "Dudelange", "lat": 49.481, "lon": 6.084},
            {"name": "Burange", "lat": 49.492, "lon": 6.083}
        ]
    },
    {
        "commune": "Rumelange",
        "canton": "Esch-sur-Alzette",
        "country": "LUX",
        "is_city": True, # Ville officielle 12/12
        "localities": [
            {"name": "Rumelange", "lat": 49.460, "lon": 6.031}
        ]
    },
    {
        "commune": "Bettembourg",
        "canton": "Esch-sur-Alzette",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Bettembourg", "lat": 49.518, "lon": 6.103},
            {"name": "Noertzange", "lat": 49.511, "lon": 6.059},
            {"name": "Huncherange", "lat": 49.518, "lon": 6.061}
        ]
    },
    {
        "commune": "Frisange",
        "canton": "Esch-sur-Alzette",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Frisange", "lat": 49.516, "lon": 6.190},
            {"name": "Aspelt", "lat": 49.522, "lon": 6.225},
            {"name": "Hellange", "lat": 49.507, "lon": 6.151}
        ]
    },
    {
        "commune": "Kayl",
        "canton": "Esch-sur-Alzette",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Kayl", "lat": 49.492, "lon": 6.039},
            {"name": "Tétange", "lat": 49.475, "lon": 6.042}
        ]
    },
    {
        "commune": "Leudelange",
        "canton": "Esch-sur-Alzette",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Leudelange", "lat": 49.567, "lon": 6.066}
        ]
    },
    {
        "commune": "Mondercange",
        "canton": "Esch-sur-Alzette",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Mondercange", "lat": 49.533, "lon": 5.989},
            {"name": "Pontpierre", "lat": 49.534, "lon": 6.031},
            {"name": "Bergem", "lat": 49.524, "lon": 6.046}
        ]
    },
    {
        "commune": "Pétange",
        "canton": "Esch-sur-Alzette",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Pétange", "lat": 49.556, "lon": 5.875},
            {"name": "Rodange", "lat": 49.546, "lon": 5.841},
            {"name": "Lamadelaine", "lat": 49.549, "lon": 5.858}
        ]
    },
    {
        "commune": "Reckange-sur-Mess",
        "canton": "Esch-sur-Alzette",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Reckange-sur-Mess", "lat": 49.562, "lon": 6.009},
            {"name": "Ehlange", "lat": 49.553, "lon": 6.018}
        ]
    },
    {
        "commune": "Roeser",
        "canton": "Esch-sur-Alzette",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Roeser", "lat": 49.537, "lon": 6.146},
            {"name": "Crauthem", "lat": 49.535, "lon": 6.136},
            {"name": "Peppange", "lat": 49.526, "lon": 6.131}
        ]
    },
    {
        "commune": "Sanem",
        "canton": "Esch-sur-Alzette",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Sanem", "lat": 49.548, "lon": 5.930},
            {"name": "Belvaux", "lat": 49.511, "lon": 5.928},
            {"name": "Soleuvre", "lat": 49.525, "lon": 5.941}
        ]
    },
    {
        "commune": "Schifflange",
        "canton": "Esch-sur-Alzette",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Schifflange", "lat": 49.506, "lon": 6.013}
        ]
    },

    # =========================================================================
    # LUXEMBOURG : CANTON DE GREVENMACHER (Gutland)
    # =========================================================================
    {
        "commune": "Grevenmacher",
        "canton": "Grevenmacher",
        "country": "LUX",
        "is_city": True, # Ville officielle 6/12
        "localities": [
            {"name": "Grevenmacher", "lat": 49.681, "lon": 6.441}
        ]
    },
    {
        "commune": "Betzdorf",
        "canton": "Grevenmacher",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Betzdorf", "lat": 49.687, "lon": 6.350},
            {"name": "Berg", "lat": 49.691, "lon": 6.355},
            {"name": "Roodt-sur-Syre", "lat": 49.667, "lon": 6.302}
        ]
    },
    {
        "commune": "Biwer",
        "canton": "Grevenmacher",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Biwer", "lat": 49.706, "lon": 6.372},
            {"name": "Wecker", "lat": 49.699, "lon": 6.386}
        ]
    },
    {
        "commune": "Flaxweiler",
        "canton": "Grevenmacher",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Flaxweiler", "lat": 49.667, "lon": 6.344}
        ]
    },
    {
        "commune": "Junglinster",
        "canton": "Grevenmacher",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Junglinster", "lat": 49.713, "lon": 6.252},
            {"name": "Gonderange", "lat": 49.699, "lon": 6.241},
            {"name": "Bourglinster", "lat": 49.703, "lon": 6.219}
        ]
    },
    {
        "commune": "Manternach",
        "canton": "Grevenmacher",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Manternach", "lat": 49.706, "lon": 6.425},
            {"name": "Münschecker", "lat": 49.700, "lon": 6.442}
        ]
    },
    {
        "commune": "Mertert",
        "canton": "Grevenmacher",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Mertert", "lat": 49.702, "lon": 6.480},
            {"name": "Wasserbillig", "lat": 49.715, "lon": 6.502}
        ]
    },
    {
        "commune": "Wormeldange",
        "canton": "Grevenmacher",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Wormeldange", "lat": 49.610, "lon": 6.406},
            {"name": "Ahn", "lat": 49.628, "lon": 6.422},
            {"name": "Machtum", "lat": 49.657, "lon": 6.438}
        ]
    },

    # =========================================================================
    # LUXEMBOURG : CANTON DE LUXEMBOURG (Gutland)
    # =========================================================================
    {
        "commune": "Luxembourg",
        "canton": "Luxembourg",
        "country": "LUX",
        "is_city": True, # Ville officielle 8/12 (Capitale)
        "localities": [
            {"name": "Luxembourg-ville", "lat": 49.611, "lon": 6.131},
            {"name": "Kirchberg", "lat": 49.627, "lon": 6.160},
            {"name": "Limpertsberg", "lat": 49.621, "lon": 6.121},
            {"name": "Gasperich", "lat": 49.589, "lon": 6.121},
            {"name": "Bonnevoie", "lat": 49.599, "lon": 6.141},
            {"name": "Cents", "lat": 49.619, "lon": 6.164},
            {"name": "Clausen", "lat": 49.614, "lon": 6.142},
            {"name": "Grund", "lat": 49.610, "lon": 6.134},
            {"name": "Pfaffenthal", "lat": 49.617, "lon": 6.133},
            {"name": "Beggen", "lat": 49.643, "lon": 6.133},
            {"name": "Hamm", "lat": 49.611, "lon": 6.168},
            {"name": "Merl", "lat": 49.602, "lon": 6.101},
            {"name": "Belair", "lat": 49.612, "lon": 6.110},
            {"name": "Hollerich", "lat": 49.599, "lon": 6.119}
        ]
    },
    {
        "commune": "Bertrange",
        "canton": "Luxembourg",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Bertrange", "lat": 49.611, "lon": 6.050}
        ]
    },
    {
        "commune": "Contern",
        "canton": "Luxembourg",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Contern", "lat": 49.584, "lon": 6.228},
            {"name": "Moutfort", "lat": 49.584, "lon": 6.253},
            {"name": "Oetrange", "lat": 49.601, "lon": 6.259}
        ]
    },
    {
        "commune": "Hesperange",
        "canton": "Luxembourg",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Hesperange", "lat": 49.573, "lon": 6.152},
            {"name": "Alzingen", "lat": 49.568, "lon": 6.162},
            {"name": "Fentange", "lat": 49.564, "lon": 6.144},
            {"name": "Itzig", "lat": 49.586, "lon": 6.172}
        ]
    },
    {
        "commune": "Niederanven",
        "canton": "Luxembourg",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Niederanven", "lat": 49.651, "lon": 6.262},
            {"name": "Senningerberg", "lat": 49.645, "lon": 6.237},
            {"name": "Oberanven", "lat": 49.655, "lon": 6.248}
        ]
    },
    {
        "commune": "Sandweiler",
        "canton": "Luxembourg",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Sandweiler", "lat": 49.617, "lon": 6.219},
            {"name": "Findel", "lat": 49.630, "lon": 6.205}
        ]
    },
    {
        "commune": "Schuttrange",
        "canton": "Luxembourg",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Schuttrange", "lat": 49.620, "lon": 6.271},
            {"name": "Munsbach", "lat": 49.631, "lon": 6.267}
        ]
    },
    {
        "commune": "Steinsel",
        "canton": "Luxembourg",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Steinsel", "lat": 49.676, "lon": 6.124},
            {"name": "Heisdorf", "lat": 49.671, "lon": 6.138},
            {"name": "Mullendorf", "lat": 49.682, "lon": 6.130}
        ]
    },
    {
        "commune": "Strassen",
        "canton": "Luxembourg",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Strassen", "lat": 49.620, "lon": 6.073}
        ]
    },
    {
        "commune": "Walferdange",
        "canton": "Luxembourg",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Walferdange", "lat": 49.658, "lon": 6.132},
            {"name": "Helmsange", "lat": 49.654, "lon": 6.138},
            {"name": "Bereldange", "lat": 49.650, "lon": 6.125}
        ]
    },
    {
        "commune": "Weiler-la-Tour",
        "canton": "Luxembourg",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Weiler-la-Tour", "lat": 49.542, "lon": 6.202},
            {"name": "Hassel", "lat": 49.550, "lon": 6.210}
        ]
    },

    # =========================================================================
    # LUXEMBOURG : CANTON DE CAPELLEN (Gutland)
    # =========================================================================
    {
        "commune": "Mamer",
        "canton": "Capellen",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Mamer", "lat": 49.627, "lon": 6.024},
            {"name": "Capellen", "lat": 49.645, "lon": 5.990},
            {"name": "Holzem", "lat": 49.616, "lon": 5.991}
        ]
    },
    {
        "commune": "Steinfort",
        "canton": "Capellen",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Steinfort", "lat": 49.661, "lon": 5.914},
            {"name": "Kleinbettingen", "lat": 49.644, "lon": 5.918},
            {"name": "Hagen", "lat": 49.651, "lon": 5.932}
        ]
    },
    {
        "commune": "Dippach",
        "canton": "Capellen",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Dippach", "lat": 49.587, "lon": 5.983},
            {"name": "Schouweiler", "lat": 49.583, "lon": 5.957},
            {"name": "Bettange-sur-Mess", "lat": 49.576, "lon": 6.007}
        ]
    },
    {
        "commune": "Garnich",
        "canton": "Capellen",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Garnich", "lat": 49.617, "lon": 5.952},
            {"name": "Kahler", "lat": 49.635, "lon": 5.916}
        ]
    },
    {
        "commune": "Habscht",
        "canton": "Capellen",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Hobscheid", "lat": 49.689, "lon": 5.915},
            {"name": "Septfontaines", "lat": 49.701, "lon": 5.967}
        ]
    },
    {
        "commune": "Kehlen",
        "canton": "Capellen",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Kehlen", "lat": 49.669, "lon": 6.033},
            {"name": "Olm", "lat": 49.656, "lon": 6.002},
            {"name": "Nospelt", "lat": 49.673, "lon": 6.009}
        ]
    },
    {
        "commune": "Koerich",
        "canton": "Capellen",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Koerich", "lat": 49.670, "lon": 5.950},
            {"name": "Goeblange", "lat": 49.668, "lon": 5.969}
        ]
    },
    {
        "commune": "Kopstal",
        "canton": "Capellen",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Kopstal", "lat": 49.664, "lon": 6.073},
            {"name": "Bridel", "lat": 49.654, "lon": 6.088}
        ]
    },
    {
        "commune": "Käerjeng",
        "canton": "Capellen",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Bascharage", "lat": 49.567, "lon": 5.908},
            {"name": "Hautcharage", "lat": 49.576, "lon": 5.909},
            {"name": "Clemency", "lat": 49.597, "lon": 5.875}
        ]
    },

    # =========================================================================
    # LUXEMBOURG : CANTON DE MERSCH (Gutland)
    # =========================================================================
    {
        "commune": "Mersch",
        "canton": "Mersch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Mersch", "lat": 49.749, "lon": 6.106},
            {"name": "Rollingen", "lat": 49.739, "lon": 6.113},
            {"name": "Beringen", "lat": 49.757, "lon": 6.118}
        ]
    },
    {
        "commune": "Bissen",
        "canton": "Mersch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Bissen", "lat": 49.789, "lon": 6.066}
        ]
    },
    {
        "commune": "Colmar-Berg",
        "canton": "Mersch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Colmar-Berg", "lat": 49.811, "lon": 6.097}
        ]
    },
    {
        "commune": "Fischbach",
        "canton": "Mersch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Fischbach", "lat": 49.740, "lon": 6.187},
            {"name": "Angelsberg", "lat": 49.761, "lon": 6.159}
        ]
    },
    {
        "commune": "Heffingen",
        "canton": "Mersch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Heffingen", "lat": 49.769, "lon": 6.241}
        ]
    },
    {
        "commune": "Helperknapp",
        "canton": "Mersch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Boevange-sur-Attert", "lat": 49.774, "lon": 6.013},
            {"name": "Tuntange", "lat": 49.718, "lon": 6.010},
            {"name": "Ansembourg", "lat": 49.702, "lon": 6.049}
        ]
    },
    {
        "commune": "Larochette",
        "canton": "Mersch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Larochette", "lat": 49.783, "lon": 6.219},
            {"name": "Ernzen", "lat": 49.770, "lon": 6.219}
        ]
    },
    {
        "commune": "Lintgen",
        "canton": "Mersch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Lintgen", "lat": 49.721, "lon": 6.128},
            {"name": "Gosseldange", "lat": 49.723, "lon": 6.108}
        ]
    },
    {
        "commune": "Lorentzweiler",
        "canton": "Mersch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Lorentzweiler", "lat": 49.701, "lon": 6.143},
            {"name": "Hunsdorf", "lat": 49.697, "lon": 6.136}
        ]
    },
    {
        "commune": "Nommern",
        "canton": "Mersch",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Nommern", "lat": 49.794, "lon": 6.175},
            {"name": "Cruchten", "lat": 49.795, "lon": 6.131}
        ]
    },

    # =========================================================================
    # LUXEMBOURG : CANTON DE REDANGE (Gutland)
    # =========================================================================
    {
        "commune": "Redange-sur-Attert",
        "canton": "Redange",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Redange-sur-Attert", "lat": 49.765, "lon": 5.890},
            {"name": "Ospern", "lat": 49.783, "lon": 5.901}
        ]
    },
    {
        "commune": "Beckerich",
        "canton": "Redange",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Beckerich", "lat": 49.734, "lon": 5.885},
            {"name": "Hovelange", "lat": 49.724, "lon": 5.914}
        ]
    },
    {
        "commune": "Ell",
        "canton": "Redange",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Ell", "lat": 49.763, "lon": 5.852},
            {"name": "Colpach-Haut", "lat": 49.760, "lon": 5.820}
        ]
    },
    {
        "commune": "Grosbous-Wal",
        "canton": "Redange",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Grosbous", "lat": 49.826, "lon": 5.966},
            {"name": "Wahl", "lat": 49.837, "lon": 5.906}
        ]
    },
    {
        "commune": "Préizerdaul",
        "canton": "Redange",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Bettborn", "lat": 49.795, "lon": 5.937},
            {"name": "Pratz", "lat": 49.800, "lon": 5.940}
        ]
    },
    {
        "commune": "Rambrouch",
        "canton": "Redange",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Rambrouch", "lat": 49.830, "lon": 5.850},
            {"name": "Koetschette", "lat": 49.830, "lon": 5.836},
            {"name": "Arsdorf", "lat": 49.860, "lon": 5.845}
        ]
    },
    {
        "commune": "Saeul",
        "canton": "Redange",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Saeul", "lat": 49.727, "lon": 5.986}
        ]
    },
    {
        "commune": "Useldange",
        "canton": "Redange",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Useldange", "lat": 49.770, "lon": 5.981},
            {"name": "Everlange", "lat": 49.774, "lon": 5.952}
        ]
    },
    {
        "commune": "Vichten",
        "canton": "Redange",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Vichten", "lat": 49.803, "lon": 6.000}
        ]
    },

    # =========================================================================
    # LUXEMBOURG : CANTON DE REMICH (Gutland / Moselle)
    # =========================================================================
    {
        "commune": "Remich",
        "canton": "Remich",
        "country": "LUX",
        "is_city": True, # Ville officielle 7/12
        "localities": [
            {"name": "Remich", "lat": 49.544, "lon": 6.368}
        ]
    },
    {
        "commune": "Bous-Waldbredimus",
        "canton": "Remich",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Bous", "lat": 49.555, "lon": 6.329},
            {"name": "Waldbredimus", "lat": 49.558, "lon": 6.287},
            {"name": "Trintange", "lat": 49.573, "lon": 6.279}
        ]
    },
    {
        "commune": "Dalheim",
        "canton": "Remich",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Dalheim", "lat": 49.542, "lon": 6.258},
            {"name": "Filsdorf", "lat": 49.532, "lon": 6.248}
        ]
    },
    {
        "commune": "Lenningen",
        "canton": "Remich",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Lenningen", "lat": 49.601, "lon": 6.368},
            {"name": "Canach", "lat": 49.613, "lon": 6.336}
        ]
    },
    {
        "commune": "Mondorf-les-Bains",
        "canton": "Remich",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Mondorf-les-Bains", "lat": 49.505, "lon": 6.281},
            {"name": "Altwies", "lat": 49.511, "lon": 6.257},
            {"name": "Ellange", "lat": 49.522, "lon": 6.297}
        ]
    },
    {
        "commune": "Schengen",
        "canton": "Remich",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Schengen", "lat": 49.471, "lon": 6.365},
            {"name": "Remerschen", "lat": 49.491, "lon": 6.352},
            {"name": "Wellenstein", "lat": 49.524, "lon": 6.344},
            {"name": "Bech-Kleinmacher", "lat": 49.531, "lon": 6.355}
        ]
    },
    {
        "commune": "Stadtbredimus",
        "canton": "Remich",
        "country": "LUX",
        "is_city": False,
        "localities": [
            {"name": "Stadtbredimus", "lat": 49.563, "lon": 6.365},
            {"name": "Greiveldange", "lat": 49.584, "lon": 6.360}
        ]
    },

    # =========================================================================
    # MADAGASCAR : RÉGION DIANA
    # =========================================================================
    # 1. District d'Antsiranana I (Commune Urbaine de Diego-Suarez)
    {
        "commune": "Antsiranana I",
        "canton": "Antsiranana I",
        "country": "MDG",
        "is_city": True,
        "localities": [
            {"name": "Antsiranana", "lat": -12.2856, "lon": 49.2917},
            {"name": "Diego-Suarez Centre", "lat": -12.2794, "lon": 49.2914},
            {"name": "Bazarikely", "lat": -12.2810, "lon": 49.2880},
            {"name": "Tanambao", "lat": -12.2950, "lon": 49.2900},
            {"name": "Scama", "lat": -12.3020, "lon": 49.2850}
        ]
    },

    # 2. District d'Antsiranana II (Communes Rurales du Nord)
    {
        "commune": "Ramena",
        "canton": "Antsiranana II",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Ramena", "lat": -12.2417, "lon": 49.3512},
            {"name": "Orangea", "lat": -12.2350, "lon": 49.3700}
        ]
    },
    {
        "commune": "Joffreville",
        "canton": "Antsiranana II",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Joffreville (Ambohitra)", "lat": -12.4960, "lon": 49.2045},
            {"name": "Montagne d'Ambre", "lat": -12.5180, "lon": 49.1760}
        ]
    },
    {
        "commune": "Sakaramy",
        "canton": "Antsiranana II",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Sakaramy", "lat": -12.4410, "lon": 49.2430}
        ]
    },
    {
        "commune": "Bobasakoa",
        "canton": "Antsiranana II",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Bobasakoa", "lat": -12.1833, "lon": 49.2500}
        ]
    },
    {
        "commune": "Ankarongana",
        "canton": "Antsiranana II",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Ankarongana", "lat": -12.3500, "lon": 49.3000}
        ]
    },
    {
        "commune": "Antanamitarana",
        "canton": "Antsiranana II",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Antanamitarana", "lat": -12.3667, "lon": 49.2667}
        ]
    },
    {
        "commune": "Mahavanona",
        "canton": "Antsiranana II",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Mahavanona", "lat": -12.4167, "lon": 49.3833}
        ]
    },
    {
        "commune": "Sadjoavato",
        "canton": "Antsiranana II",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Sadjoavato", "lat": -12.5833, "lon": 49.3667}
        ]
    },
    {
        "commune": "Mangaoka",
        "canton": "Antsiranana II",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Mangaoka", "lat": -12.3167, "lon": 49.2167}
        ]
    },
    {
        "commune": "Andranovondronina",
        "canton": "Antsiranana II",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Andranovondronina (Cap d'Ambre)", "lat": -12.0167, "lon": 49.2833}
        ]
    },

    # 3. District d'Ambanja (Vallée du Sambirano)
    {
        "commune": "Ambanja",
        "canton": "Ambanja",
        "country": "MDG",
        "is_city": True,
        "localities": [
            {"name": "Ambanja", "lat": -13.6800, "lon": 48.4500},
            {"name": "Sambirano", "lat": -13.6600, "lon": 48.4700}
        ]
    },
    {
        "commune": "Anaborano Rivière",
        "canton": "Ambanja",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Anaborano Rivière", "lat": -13.6167, "lon": 48.5500}
        ]
    },
    {
        "commune": "Ambalahonko",
        "canton": "Ambanja",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Ambalahonko", "lat": -13.7500, "lon": 48.3833}
        ]
    },
    {
        "commune": "Antsatsaka",
        "canton": "Ambanja",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Antsatsaka", "lat": -13.6000, "lon": 48.4167}
        ]
    },
    {
        "commune": "Bemanevika",
        "canton": "Ambanja",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Bemanevika", "lat": -13.8000, "lon": 48.5167}
        ]
    },
    {
        "commune": "Maherivaratra",
        "canton": "Ambanja",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Maherivaratra", "lat": -13.5167, "lon": 48.4833}
        ]
    },
    {
        "commune": "Ambodimanga Ramena",
        "canton": "Ambanja",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Ambodimanga Ramena", "lat": -13.7167, "lon": 48.6000}
        ]
    },

    # 4. District d'Ambilobe (Plaines cannières et vivrières)
    {
        "commune": "Ambilobe",
        "canton": "Ambilobe",
        "country": "MDG",
        "is_city": True,
        "localities": [
            {"name": "Ambilobe", "lat": -12.9167, "lon": 49.0500},
            {"name": "Sirama Ambilobe", "lat": -12.9500, "lon": 49.0333}
        ]
    },
    {
        "commune": "Anivorano Nord",
        "canton": "Ambilobe",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Anivorano Nord", "lat": -12.7486, "lon": 49.2394},
            {"name": "Lac Sacré Anivorano", "lat": -12.7400, "lon": 49.2450}
        ]
    },
    {
        "commune": "Beramanja",
        "canton": "Ambilobe",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Beramanja", "lat": -13.0500, "lon": 48.9167}
        ]
    },
    {
        "commune": "Betsiaka",
        "canton": "Ambilobe",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Betsiaka", "lat": -13.0833, "lon": 49.2500}
        ]
    },
    {
        "commune": "Mahamasina",
        "canton": "Ambilobe",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Mahamasina (Ankarana)", "lat": -12.9667, "lon": 49.1333}
        ]
    },
    {
        "commune": "Matsaborola",
        "canton": "Ambilobe",
        "country": "MDG",
        "is_city": False,
        "localities": [
            {"name": "Matsaborola", "lat": -13.1167, "lon": 49.0167}
        ]
    },

    # 5. District de Nosy Be (Île aux parfums)
    {
        "commune": "Nosy Be",
        "canton": "Nosy Be",
        "country": "MDG",
        "is_city": True,
        "localities": [
            {"name": "Hell-Ville (Andoany)", "lat": -13.4000, "lon": 48.2667},
            {"name": "Dzamandzar", "lat": -13.3167, "lon": 48.2167},
            {"name": "Ampasindava", "lat": -13.4333, "lon": 48.2500},
            {"name": "Befotaka", "lat": -13.2500, "lon": 48.2833},
            {"name": "Ambatozavavy", "lat": -13.3667, "lon": 48.3167},
            {"name": "Ambatoloaka", "lat": -13.3750, "lon": 48.2350}
        ]
    }
]

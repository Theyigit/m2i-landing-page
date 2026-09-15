"""
Per-country facts behind the generated "Moving to Ireland from X" guides.

Each row: name, slug fragment, whether the name takes "the", adjective,
region, then the facts the article branches on. Keep the sets below in
step with the official lists they mirror; the sources are named next to
each one.

  visa     eea      EU/EEA/Swiss citizen: free movement, no visa or permit
           free     not visa required (irishimmigration.ie list), 90 days
           required visa required: long stay D visa before travel
  licence  eu       EU/EEA/Swiss licence, drive on it, swap when it expires
           exchange NDLS recognised state, exchange without a test
           none     not recognised: theory test, learner permit, EDT, test
  dta      Ireland has a double taxation agreement in effect (Revenue list)
  ssa      bilateral social security agreement (gov.ie list); EEA/CH via EU rules
  wha      Working Holiday Authorisation partner (DFA list)
  pets     eu | listed (EU Reg 577/2013 Annex II) | unlisted (titre test)
  direct   direct flights from Dublin are the normal way home
"""

# (name, slug, the, adjective, region, visa, licence, dta, ssa, wha, pets, currency, direct)
ROWS = [
    # --- EU, EEA and Switzerland -------------------------------------------
    ("Austria", "austria", 0, "Austrian", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("Belgium", "belgium", 0, "Belgian", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("Bulgaria", "bulgaria", 0, "Bulgarian", "eu", "eea", "eu", 1, 1, 0, "eu", "the lev", 1),
    ("Croatia", "croatia", 0, "Croatian", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("Cyprus", "cyprus", 0, "Cypriot", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("the Czech Republic", "the-czech-republic", 1, "Czech", "eu", "eea", "eu", 1, 1, 0, "eu", "the Czech koruna", 1),
    ("Denmark", "denmark", 0, "Danish", "eu", "eea", "eu", 1, 1, 0, "eu", "the Danish krone", 1),
    ("Estonia", "estonia", 0, "Estonian", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("Finland", "finland", 0, "Finnish", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("France", "france", 0, "French", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("Germany", "germany", 0, "German", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("Greece", "greece", 0, "Greek", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("Hungary", "hungary", 0, "Hungarian", "eu", "eea", "eu", 1, 1, 0, "eu", "the forint", 1),
    ("Iceland", "iceland", 0, "Icelandic", "eu", "eea", "eu", 1, 1, 0, "eu", "the Icelandic króna", 1),
    ("Italy", "italy", 0, "Italian", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("Latvia", "latvia", 0, "Latvian", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("Lithuania", "lithuania", 0, "Lithuanian", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("Luxembourg", "luxembourg", 0, "Luxembourgish", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("Malta", "malta", 0, "Maltese", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("the Netherlands", "the-netherlands", 1, "Dutch", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("Norway", "norway", 0, "Norwegian", "eu", "eea", "eu", 1, 1, 0, "eu", "the Norwegian krone", 1),
    ("Poland", "poland", 0, "Polish", "eu", "eea", "eu", 1, 1, 0, "eu", "the złoty", 1),
    ("Portugal", "portugal", 0, "Portuguese", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("Romania", "romania", 0, "Romanian", "eu", "eea", "eu", 1, 1, 0, "eu", "the leu", 1),
    ("Slovakia", "slovakia", 0, "Slovak", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("Slovenia", "slovenia", 0, "Slovenian", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 0),
    ("Spain", "spain", 0, "Spanish", "eu", "eea", "eu", 1, 1, 0, "eu", "the euro", 1),
    ("Sweden", "sweden", 0, "Swedish", "eu", "eea", "eu", 1, 1, 0, "eu", "the Swedish krona", 1),
    ("Switzerland", "switzerland", 0, "Swiss", "eu", "eea", "exchange", 1, 1, 0, "eu", "the Swiss franc", 1),
    # --- Rest of Europe and the Caucasus ------------------------------------
    ("Albania", "albania", 0, "Albanian", "europe", "required", "none", 1, 0, 0, "unlisted", "the lek", 0),
    ("Armenia", "armenia", 0, "Armenian", "europe", "required", "none", 1, 0, 0, "unlisted", "the dram", 0),
    ("Azerbaijan", "azerbaijan", 0, "Azerbaijani", "europe", "required", "none", 0, 0, 0, "unlisted", "the manat", 0),
    ("Belarus", "belarus", 0, "Belarusian", "europe", "required", "none", 1, 0, 0, "listed", "the Belarusian rouble", 0),
    ("Bosnia and Herzegovina", "bosnia-and-herzegovina", 0, "Bosnian", "europe", "required", "none", 1, 0, 0, "listed", "the convertible mark", 0),
    ("Georgia", "georgia", 0, "Georgian", "europe", "required", "none", 1, 0, 0, "unlisted", "the lari", 0),
    ("Kosovo", "kosovo", 0, "Kosovar", "europe", "required", "none", 1, 0, 0, "unlisted", "the euro", 0),
    ("Moldova", "moldova", 0, "Moldovan", "europe", "required", "none", 1, 0, 0, "unlisted", "the Moldovan leu", 0),
    ("North Macedonia", "north-macedonia", 0, "Macedonian", "europe", "required", "none", 1, 0, 0, "listed", "the denar", 0),
    ("Russia", "russia", 0, "Russian", "europe", "required", "none", "suspended", 0, 0, "listed", "the rouble", 0),
    ("Serbia", "serbia", 0, "Serbian", "europe", "required", "none", 1, 0, 0, "unlisted", "the dinar", 0),
    ("Turkey", "turkey", 0, "Turkish", "europe", "required", "none", 1, 0, 0, "unlisted", "the Turkish lira", 1),
    ("Ukraine", "ukraine", 0, "Ukrainian", "europe", "ukraine", "ukraine", 1, 0, 0, "unlisted", "the hryvnia", 0),
    # --- Middle East and North Africa ---------------------------------------
    ("Algeria", "algeria", 0, "Algerian", "mena", "required", "none", 0, 0, 0, "unlisted", "the Algerian dinar", 0),
    ("Bahrain", "bahrain", 0, "Bahraini", "mena", "required", "none", 1, 0, 0, "listed", "the Bahraini dinar", 0),
    ("Egypt", "egypt", 0, "Egyptian", "mena", "required", "none", 1, 0, 0, "unlisted", "the Egyptian pound", 0),
    ("Iran", "iran", 0, "Iranian", "mena", "required", "none", 0, 0, 0, "unlisted", "the rial", 0),
    ("Iraq", "iraq", 0, "Iraqi", "mena", "required", "none", 0, 0, 0, "unlisted", "the Iraqi dinar", 0),
    ("Israel", "israel", 0, "Israeli", "mena", "free", "none", 1, 0, 0, "unlisted", "the shekel", 0),
    ("Jordan", "jordan", 0, "Jordanian", "mena", "required", "none", 0, 0, 0, "unlisted", "the Jordanian dinar", 0),
    ("Kuwait", "kuwait", 0, "Kuwaiti", "mena", "required", "none", 1, 0, 0, "unlisted", "the Kuwaiti dinar", 0),
    ("Lebanon", "lebanon", 0, "Lebanese", "mena", "required", "none", 0, 0, 0, "unlisted", "the Lebanese pound", 0),
    ("Morocco", "morocco", 0, "Moroccan", "mena", "required", "none", 1, 0, 0, "unlisted", "the dirham", 1),
    ("Oman", "oman", 0, "Omani", "mena", "required", "none", 0, 0, 0, "unlisted", "the Omani rial", 0),
    ("Qatar", "qatar", 0, "Qatari", "mena", "required", "none", 1, 0, 0, "unlisted", "the Qatari riyal", 1),
    ("Saudi Arabia", "saudi-arabia", 0, "Saudi", "mena", "required", "none", 1, 0, 0, "unlisted", "the Saudi riyal", 0),
    ("Tunisia", "tunisia", 0, "Tunisian", "mena", "required", "none", 0, 0, 0, "unlisted", "the Tunisian dinar", 0),
    ("the UAE", "the-uae", 1, "Emirati", "mena", "free", "none", 1, 0, 0, "listed", "the UAE dirham", 1),
    # --- Sub-Saharan Africa -------------------------------------------------
    ("Angola", "angola", 0, "Angolan", "africa", "required", "none", 0, 0, 0, "unlisted", "the kwanza", 0),
    ("Benin", "benin", 0, "Beninese", "africa", "required", "none", 0, 0, 0, "unlisted", "the West African CFA franc", 0),
    ("Botswana", "botswana", 0, "Botswanan", "africa", "required", "none", 1, 0, 0, "unlisted", "the pula", 0),
    ("Burkina Faso", "burkina-faso", 0, "Burkinabè", "africa", "required", "none", 0, 0, 0, "unlisted", "the West African CFA franc", 0),
    ("Burundi", "burundi", 0, "Burundian", "africa", "required", "none", 0, 0, 0, "unlisted", "the Burundian franc", 0),
    ("Cameroon", "cameroon", 0, "Cameroonian", "africa", "required", "none", 0, 0, 0, "unlisted", "the Central African CFA franc", 0),
    ("the Central African Republic", "the-central-african-republic", 1, "Central African", "africa", "required", "none", 0, 0, 0, "unlisted", "the Central African CFA franc", 0),
    ("Chad", "chad", 0, "Chadian", "africa", "required", "none", 0, 0, 0, "unlisted", "the Central African CFA franc", 0),
    ("the Republic of the Congo", "the-republic-of-the-congo", 1, "Congolese", "africa", "required", "none", 0, 0, 0, "unlisted", "the Central African CFA franc", 0),
    ("the Democratic Republic of the Congo", "the-democratic-republic-of-the-congo", 1, "Congolese", "africa", "required", "none", 0, 0, 0, "unlisted", "the Congolese franc", 0),
    ("Côte d'Ivoire", "cote-divoire", 0, "Ivorian", "africa", "required", "none", 0, 0, 0, "unlisted", "the West African CFA franc", 0),
    ("Equatorial Guinea", "equatorial-guinea", 0, "Equatoguinean", "africa", "required", "none", 0, 0, 0, "unlisted", "the Central African CFA franc", 0),
    ("Eswatini", "eswatini", 0, "Swazi", "africa", "free", "none", 0, 0, 0, "unlisted", "the lilangeni", 0),
    ("Ethiopia", "ethiopia", 0, "Ethiopian", "africa", "required", "none", 1, 0, 0, "unlisted", "the birr", 0),
    ("Gabon", "gabon", 0, "Gabonese", "africa", "required", "none", 0, 0, 0, "unlisted", "the Central African CFA franc", 0),
    ("the Gambia", "the-gambia", 1, "Gambian", "africa", "required", "none", 0, 0, 0, "unlisted", "the dalasi", 0),
    ("Ghana", "ghana", 0, "Ghanaian", "africa", "required", "none", 1, 0, 0, "unlisted", "the cedi", 0),
    ("Guinea", "guinea", 0, "Guinean", "africa", "required", "none", 0, 0, 0, "unlisted", "the Guinean franc", 0),
    ("Guinea-Bissau", "guinea-bissau", 0, "Bissau-Guinean", "africa", "required", "none", 0, 0, 0, "unlisted", "the West African CFA franc", 0),
    ("Kenya", "kenya", 0, "Kenyan", "africa", "required", "none", 1, 0, 0, "unlisted", "the Kenyan shilling", 0),
    ("Lesotho", "lesotho", 0, "Basotho", "africa", "free", "none", 0, 0, 0, "unlisted", "the loti", 0),
    ("Liberia", "liberia", 0, "Liberian", "africa", "required", "none", 0, 0, 0, "unlisted", "the Liberian dollar", 0),
    ("Madagascar", "madagascar", 0, "Malagasy", "africa", "required", "none", 0, 0, 0, "unlisted", "the ariary", 0),
    ("Malawi", "malawi", 0, "Malawian", "africa", "free", "none", 0, 0, 0, "unlisted", "the kwacha", 0),
    ("Mali", "mali", 0, "Malian", "africa", "required", "none", 0, 0, 0, "unlisted", "the West African CFA franc", 0),
    ("Mauritania", "mauritania", 0, "Mauritanian", "africa", "required", "none", 0, 0, 0, "unlisted", "the ouguiya", 0),
    ("Mauritius", "mauritius", 0, "Mauritian", "africa", "free", "none", 0, 0, 0, "listed", "the Mauritian rupee", 0),
    ("Mozambique", "mozambique", 0, "Mozambican", "africa", "required", "none", 0, 0, 0, "unlisted", "the metical", 0),
    ("Namibia", "namibia", 0, "Namibian", "africa", "required", "none", 0, 0, 0, "unlisted", "the Namibian dollar", 0),
    ("Niger", "niger", 0, "Nigerien", "africa", "required", "none", 0, 0, 0, "unlisted", "the West African CFA franc", 0),
    ("Rwanda", "rwanda", 0, "Rwandan", "africa", "required", "none", 0, 0, 0, "unlisted", "the Rwandan franc", 0),
    ("Senegal", "senegal", 0, "Senegalese", "africa", "required", "none", 0, 0, 0, "unlisted", "the West African CFA franc", 0),
    ("Sierra Leone", "sierra-leone", 0, "Sierra Leonean", "africa", "required", "none", 0, 0, 0, "unlisted", "the leone", 0),
    ("Somalia", "somalia", 0, "Somali", "africa", "required", "none", 0, 0, 0, "unlisted", "the Somali shilling", 0),
    ("South Sudan", "south-sudan", 0, "South Sudanese", "africa", "required", "none", 0, 0, 0, "unlisted", "the South Sudanese pound", 0),
    ("Sudan", "sudan", 0, "Sudanese", "africa", "required", "none", 0, 0, 0, "unlisted", "the Sudanese pound", 0),
    ("Tanzania", "tanzania", 0, "Tanzanian", "africa", "required", "none", 0, 0, 0, "unlisted", "the Tanzanian shilling", 0),
    ("Togo", "togo", 0, "Togolese", "africa", "required", "none", 0, 0, 0, "unlisted", "the West African CFA franc", 0),
    ("Uganda", "uganda", 0, "Ugandan", "africa", "required", "none", 0, 0, 0, "unlisted", "the Ugandan shilling", 0),
    ("Zambia", "zambia", 0, "Zambian", "africa", "required", "none", 1, 0, 0, "unlisted", "the Zambian kwacha", 0),
    ("Zimbabwe", "zimbabwe", 0, "Zimbabwean", "africa", "required", "none", 0, 0, 0, "unlisted", "the Zimbabwe gold (ZiG) and the US dollar", 0),
    # --- Asia ---------------------------------------------------------------
    ("Bangladesh", "bangladesh", 0, "Bangladeshi", "asia", "required", "none", 0, 0, 0, "unlisted", "the taka", 0),
    ("Cambodia", "cambodia", 0, "Cambodian", "asia", "required", "none", 0, 0, 0, "unlisted", "the riel and the US dollar", 0),
    ("China", "china", 0, "Chinese", "asia", "required", "none", 1, 0, 0, "unlisted", "the renminbi", 0),
    ("Hong Kong", "hong-kong", 0, "Hong Kong", "asia", "free", "none", 1, 0, 1, "listed", "the Hong Kong dollar", 0),
    ("Indonesia", "indonesia", 0, "Indonesian", "asia", "required", "none", 0, 0, 0, "unlisted", "the rupiah", 0),
    ("Japan", "japan", 0, "Japanese", "asia", "free", "exchange", 1, 1, 1, "listed", "the yen", 0),
    ("Kazakhstan", "kazakhstan", 0, "Kazakh", "asia", "required", "none", 1, 0, 0, "unlisted", "the tenge", 0),
    ("Kyrgyzstan", "kyrgyzstan", 0, "Kyrgyz", "asia", "required", "none", 0, 0, 0, "unlisted", "the som", 0),
    ("Laos", "laos", 0, "Lao", "asia", "required", "none", 0, 0, 0, "unlisted", "the kip", 0),
    ("Malaysia", "malaysia", 0, "Malaysian", "asia", "free", "none", 1, 0, 0, "listed", "the ringgit", 0),
    ("Mongolia", "mongolia", 0, "Mongolian", "asia", "required", "none", 0, 0, 0, "unlisted", "the tögrög", 0),
    ("Myanmar", "myanmar", 0, "Myanmar", "asia", "required", "none", 0, 0, 0, "unlisted", "the kyat", 0),
    ("Nepal", "nepal", 0, "Nepali", "asia", "required", "none", 0, 0, 0, "unlisted", "the Nepalese rupee", 0),
    ("Pakistan", "pakistan", 0, "Pakistani", "asia", "required", "none", 1, 0, 0, "unlisted", "the Pakistani rupee", 0),
    ("Singapore", "singapore", 0, "Singaporean", "asia", "free", "none", 1, 0, 0, "listed", "the Singapore dollar", 0),
    ("South Korea", "south-korea", 0, "South Korean", "asia", "free", "exchange", 1, 1, 1, "unlisted", "the won", 0),
    ("Sri Lanka", "sri-lanka", 0, "Sri Lankan", "asia", "required", "none", 0, 0, 0, "unlisted", "the Sri Lankan rupee", 0),
    ("Taiwan", "taiwan", 0, "Taiwanese", "asia", "free", "exchange", 0, 0, 1, "listed", "the New Taiwan dollar", 0),
    ("Tajikistan", "tajikistan", 0, "Tajik", "asia", "required", "none", 0, 0, 0, "unlisted", "the somoni", 0),
    ("Thailand", "thailand", 0, "Thai", "asia", "required", "none", 1, 0, 0, "unlisted", "the baht", 0),
    ("Timor-Leste", "timor-leste", 0, "Timorese", "asia", "required", "none", 0, 0, 0, "unlisted", "the US dollar", 0),
    ("Turkmenistan", "turkmenistan", 0, "Turkmen", "asia", "required", "none", 0, 0, 0, "unlisted", "the Turkmen manat", 0),
    ("Uzbekistan", "uzbekistan", 0, "Uzbek", "asia", "required", "none", 1, 0, 0, "unlisted", "the so'm", 0),
    ("Vietnam", "vietnam", 0, "Vietnamese", "asia", "required", "none", 1, 0, 0, "unlisted", "the đồng", 0),
    # --- Oceania ------------------------------------------------------------
    ("New Zealand", "new-zealand", 0, "New Zealand", "oceania", "free", "exchange", 1, 1, 1, "listed", "the New Zealand dollar", 0),
    ("Papua New Guinea", "papua-new-guinea", 0, "Papua New Guinean", "oceania", "required", "none", 0, 0, 0, "unlisted", "the kina", 0),
    # --- The Americas -------------------------------------------------------
    ("Argentina", "argentina", 0, "Argentine", "americas", "free", "none", 0, 0, 1, "listed", "the Argentine peso", 0),
    ("Bolivia", "bolivia", 0, "Bolivian", "americas", "required", "none", 0, 0, 0, "unlisted", "the boliviano", 0),
    ("Chile", "chile", 0, "Chilean", "americas", "free", "none", 1, 0, 1, "listed", "the Chilean peso", 0),
    ("Colombia", "colombia", 0, "Colombian", "americas", "required", "none", 0, 0, 0, "unlisted", "the Colombian peso", 0),
    ("Costa Rica", "costa-rica", 0, "Costa Rican", "americas", "free", "none", 0, 0, 0, "unlisted", "the colón", 0),
    ("Cuba", "cuba", 0, "Cuban", "americas", "required", "none", 0, 0, 0, "unlisted", "the Cuban peso", 0),
    ("the Dominican Republic", "the-dominican-republic", 1, "Dominican", "americas", "required", "none", 0, 0, 0, "unlisted", "the Dominican peso", 0),
    ("Ecuador", "ecuador", 0, "Ecuadorian", "americas", "required", "none", 0, 0, 0, "unlisted", "the US dollar", 0),
    ("El Salvador", "el-salvador", 0, "Salvadoran", "americas", "free", "none", 0, 0, 0, "unlisted", "the US dollar", 0),
    ("Guatemala", "guatemala", 0, "Guatemalan", "americas", "free", "none", 0, 0, 0, "unlisted", "the quetzal", 0),
    ("Haiti", "haiti", 0, "Haitian", "americas", "required", "none", 0, 0, 0, "unlisted", "the gourde", 0),
    ("Honduras", "honduras", 0, "Honduran", "americas", "required", "none", 0, 0, 0, "unlisted", "the lempira", 0),
    ("Jamaica", "jamaica", 0, "Jamaican", "americas", "required", "none", 0, 0, 0, "listed", "the Jamaican dollar", 0),
    ("Mexico", "mexico", 0, "Mexican", "americas", "free", "none", 1, 0, 0, "listed", "the Mexican peso", 0),
    ("Nicaragua", "nicaragua", 0, "Nicaraguan", "americas", "free", "none", 0, 0, 0, "unlisted", "the córdoba", 0),
    ("Panama", "panama", 0, "Panamanian", "americas", "free", "none", 1, 0, 0, "unlisted", "the balboa and the US dollar", 0),
    ("Paraguay", "paraguay", 0, "Paraguayan", "americas", "free", "none", 0, 0, 0, "unlisted", "the guaraní", 0),
    ("Peru", "peru", 0, "Peruvian", "americas", "required", "none", 0, 0, 0, "unlisted", "the sol", 0),
    ("Trinidad and Tobago", "trinidad-and-tobago", 0, "Trinidadian and Tobagonian", "americas", "free", "none", 0, 0, 0, "listed", "the Trinidad and Tobago dollar", 0),
    ("Uruguay", "uruguay", 0, "Uruguayan", "americas", "free", "none", 0, 0, 0, "unlisted", "the Uruguayan peso", 0),
    ("Venezuela", "venezuela", 0, "Venezuelan", "americas", "required", "none", 0, 0, 0, "unlisted", "the bolívar", 0),
]

FIELDS = ("name", "slug", "the", "adjective", "region", "visa", "licence", "dta", "ssa", "wha", "pets", "currency", "direct")

REGIONS = {
    "eu": "EU, EEA and Switzerland",
    "europe": "Rest of Europe",
    "mena": "Middle East and North Africa",
    "africa": "Sub-Saharan Africa",
    "asia": "Asia",
    "oceania": "Oceania",
    "americas": "Latin America and the Caribbean",
}

COUNTRIES = [dict(zip(FIELDS, r)) for r in ROWS]
assert len({c["slug"] for c in COUNTRIES}) == len(COUNTRIES)

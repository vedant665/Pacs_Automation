"""
company_onboarding_data.py
---------------------------
Test data for Company Onboarding screen.
"""

import random
import string
import uuid
from datetime import datetime


# ================================================================
# 0. VALID ADDRESS DATA (State → District → Taluka)
# ================================================================
COMPANY_BACKGROUNDS = [
    "Software development and IT consulting services",
    "Manufacturing and industrial solutions",
    "Financial services and banking operations",
    "Healthcare and pharmaceutical research",
    "E-commerce and digital retail platforms",
    "Telecommunications and networking infrastructure",
    "Education and e-learning technology solutions",
    "Logistics and supply chain management",
    "Real estate and construction development",
    "Agriculture and food processing industries",
]


# ================================================================
# PROMOTER DATA (random 1 per company)
# ================================================================
PROMOTER_DATA = [
    {"name": "Mr Chaitnya Namdev Chavhan", "remark": "Mr Chavhan."},
    {"name": "Mr Durgesh Vishnu Bankar", "remark": "Mr Bankar."},
    {"name": "Mr Amit Ramesh Sharma", "remark": "Mr Sharma."},
    {"name": "Mr Suresh Dnyaneshwar Patil", "remark": "Mr Patil."},
    {"name": "Mr Rajesh Bhimrao Jadhav", "remark": "Mr Jadhav."},
    {"name": "Mr Vikram Anil Deshmukh", "remark": "Mr Deshmukh."},
]

# ================================================================
# BUSINESS DETAILS (fixed values from mentor)
# ================================================================
BUSINESS_MODEL = "Agri-Input - Products and materials."

MARKET_LINKAGES = "Market linkage involves connecting farmers."

LINE_OF_BUSINESS = "Products and materials used by farmers."

ADDITIONAL_BUSINESS_ACTIVITIES = "FPC carries out the business of Production."

# ================================================================
# INFRASTRUCTURE DATA
# ================================================================
INFRASTRUCTURE_LOCATIONS = [
    "Main Market Yard, Agricultural Produce",
    "Rural Hub Center, District HQ",
    "Cooperative Society Building, Taluka",
    "Agricultural Processing Unit, Industrial Area",
    "FPC Operations Center, Village Panchayat",
]




ADDRESS_DATA = {
    "ANDHRA PRADESH": {
        "CHITTOOR": ["Baireddipalle", "Bangarupalem"],
        "EAST GODAVARI": ["Anaparthi", "Biccavolu", "Chagallu"],
        "GUNTUR": ["Amaravathi", "Amruthalur", "Atchampet", "Bapatla", "Bellamkonda", "Bhattiprolu", "Bollapalle", "Chebrolu", "Cherukupalle H/O Arumbaka", "Chilakaluripet H/O.Purushotha Patnam", "Dachepalle", "Duggirala", "Durgi", "Edlapadu", "GUNTUR EAST", "Guntur", "Gurazala", "Ipur", "Kakumanu", "Karempudi", "Karlapalem", "Kollipara", "Kollur", "Krosuru", "Machavaram", "Macherla", "Mangalagiri", "Medikonduru", "Muppalla", "Nadendla", "Nagaram", "Narasaraopet", "Nekarikallu", "Nizampatnam", "Nuzendla", "Pedakakani", "Pedakurapadu", "Pedanandipadu", "Phirangipuram", "Piduguralla", "Pittalavanipalem", "Ponnur", "Prathipadu", "Rajupalem", "Rentachintala", "Repalle", "Rompicherla", "Sattenapalle", "Savalyapuram H/O Kanamarlapudi", "Tadepalle", "Tadikonda", "Tenali", "Thullur", "Tsundur", "Vatticherukuru", "Veldurthi", "Vemuru", "Vinukonda"],
        "KRISHNA": ["Avanigadda", "Bantumilli"],
        "Visakhapatnam": ["Anandapuram", "Bheemunipatnam"],
        "Y.S.R.": ["Atlur", "B.Kodur"],
    },

    "GUJARAT": {
        "AHMADABAD": ["Asarva", "Bavla", "Daskroi", "Detroj-Rampura", "Dhandhuka", "Dholera", "Dholka", "Ghatlodiya", "Mandal", "Maninagar", "Sabarmati", "Sanand", "Vatva", "Vejalpur", "Viramgam"],
        "AMRELI": ["Amreli", "Babra"],
        "ANAND": ["Anand City", "Anand Rural", "Anklav", "Borsad", "Khambhat", "Petlad", "Sojitra", "Tarapur", "Umreth"],
        "ARVALLI": ["Bayad", "Bhiloda", "Dhansura", "Malpur", "Meghraj", "Modasa"],
        "BANAS KANTHA": ["Amirgadh", "Bhabhar", "Danta", "Dantiwada", "Deesa", "Deodar", "Dhanera", "Kankrej", "Lakhani", "Palanpur", "SUIGAM", "Tharad", "Vadgam", "Vav"],
        "BHARUCH": ["Amod", "Anklesvar", "Bharuch", "Hansot", "Jambusar", "Jhagadia", "Netrang", "Vagra", "Valia"],
        "BHAVNAGAR": ["Bhavnagar", "Gariadhar", "Ghogha", "Jesar", "Mahuva", "Palitana", "Sihor", "Talaja", "Umrala", "Vallabhipur"],
        "BOTAD": ["Barwala", "Botad", "Gadhada", "Ranpur"],
        "CHHOTAUDEPUR": ["BODELI", "Chhota Udaipur", "Jetpur Pavi", "Kavant", "Nasvadi", "Sankheda"],
        "DANG": ["Ahwa", "Subir", "Waghai"],
        "DEVBHUMI DWARKA": ["Bhanvad", "Kalyanpur", "Khambhalia", "Okhamandal"],
        "DOHAD": ["Devgadbaria", "Dhanpur", "Dohad", "Fatepura", "Garbada", "Jhalod", "Limkheda", "Sanjeli", "Singvad"],
        "GANDHINAGAR": ["Dehgam", "Gandhinagar", "Kalol Gandhinagar", "Mansa"],
        "GIR SOMNATH": ["Gir Gadhda", "Kodinar", "Patan-Veraval", "Sutrapada", "Talala", "Una"],
        "JAMNAGAR": ["Dhrol", "Jamjodhpur", "Jamnagar City", "Jamnagar Rural", "Jodiya", "Kalavad", "Lalpur"],
        "JUNAGADH": ["Bhesan", "Junagadh", "Junagadh City", "Keshod", "Malia Hatina", "Manavadar", "Mangrol", "Mendarda", "Vanthali", "Visavadar"],
        "KACHCHH": ["Abdasa", "Anjar", "Bhachau", "Bhuj", "Gandhidham", "Lakhpat", "Mandvi", "Mundra", "Nakhatrana", "Rapar"],
        "KHEDA": ["Galteshwar", "Kapadvanj", "Kathlal", "Kheda", "Mahudha", "Matar", "Mehmedabad", "Nadiad", "Nadiad City", "Thasra", "Vaso"],
        "MAHESANA": ["Becharaji", "Jotana", "Kadi", "Kheralu", "Mahesana", "Satlasana", "Unjha", "Vadnagar", "Vijapur", "Visnagar"],
        "MORBI": ["Halvad", "Maliya", "Morvi", "Tankara", "Wankaner"],
        "Mahisagar": ["Balasinor", "Kadana", "Khanpur", "Lunawada", "Santrampur", "Virpur"],
        "NARMADA": ["Dediapada", "GARUDESHWAR", "Nandod", "Sagbara", "Tilakwada"],
        "NAVSARI": ["Bansda", "Chikhli", "Gandevi", "Jalalpore", "Khergam", "Navsari"],
        "PANCH MAHALS": ["Ghoghamba", "Godhra", "Halol", "Jambughoda", "Kalol", "Morwa (Hadaf)", "Shehera"],
        "PATAN": ["Chanasma", "Harij", "Patan", "Radhanpur", "Sami", "Santalpur", "Saraswati", "Shankheshvar", "Sidhpur"],
        "PORBANDAR": ["Kutiyana", "Porbandar", "Ranavav"],
        "RAJKOT": ["Dhoraji", "Gondal", "Jamkandorna", "Jasdan", "Jetpur", "Kotda Sangani", "Lodhika", "Paddhari", "RAJKOT EAST", "RAJKOT SOUTH", "RAJKOT WEST", "Rajkot", "Upleta", "Vinchchiya"],
        "SABAR KANTHA": ["Himatnagar", "Idar", "Khedbrahma", "POSHINA", "Prantij", "Talod", "Vadali", "Vijaynagar"],
        "SURAT": ["Adajan", "Bardoli", "Chorasi", "Kamrej", "Katargam", "Mahuva", "Majura", "Mandvi surat", "Mangrol", "Olpad", "Palsana", "Puna", "Udhna", "Umarpada"],
        "SURENDRANAGAR": ["Chotila", "Chuda", "Dasada", "Dhrangadhra", "Lakhtar", "Limbdi", "Muli", "Sayla", "Thangadh", "Wadhwan"],
        "TAPI": ["Dolvan", "Kukarmunda", "Nizar", "Songadh", "Uchchhal", "Valod", "Vyara"],
        "VADODARA": ["DESAR", "Dabhoi", "Karjan", "Padra", "Savli", "Sinor", "Vadodara East", "Vadodara North", "Vadodara Rural", "Vadodara South", "Vadodara West", "Vaghodia"],
        "VALSAD": ["Dharampur", "Kaprada", "Pardi", "Umbergaon", "VAPI", "Valsad"],
    },
    "KARNATAKA": {
        "BAGALKOTE": ["Badami", "Bagalkot", "Bilgi", "GULEDGUDDA", "Hungund", "ILKAL", "Jamkhandi", "Mudhol", "RABAKAVI BANAHATTI"],
        "BALLARI": ["Ballari", "Hadagalli", "Hagaribommanahalli", "Harapanahalli", "Hosapete", "KAMPLI", "KOTTURU", "KURUGODU", "Kudligi", "Sandur", "Siruguppa"],
        "BELAGAVI": ["Athni", "BELAGAVI", "Bailahongala", "Chikodi", "Gokak", "Hukeri", "KAGWAD", "KITTUR", "Khanapur", "MUDALGI", "NIPPANI", "Ramdurg", "Raybag", "SAVADATTI"],
        "BENGALURU RURAL": ["Devanahalli", "Dodda Ballapur", "Hosakote", "Nelamangala"],
        "BENGALURU URBAN": ["Anekal", "Bengaluru East", "Bengaluru North", "Bengaluru South", "YELAHANKA"],
        "BIDAR": ["Aurad", "Basavakalyan", "Bhalki", "Bidar", "CHITAGUPPA", "HULSOOR", "Homnabad", "KAMALNAGAR"],
        "CHAMARAJANAGARA": ["Chamarajanagar", "Gundlupet", "HANUR", "Kollegal", "Yelandur"],
        "CHIKKABALLAPURA": ["Bagepalli", "Chikkaballapura", "Chintamani", "Gauribidanur", "Gudibanda", "Sidlaghatta"],
        "CHIKKAMAGALURU": ["AJJAMPURA", "Chikkamagaluru", "Kadur", "Koppa", "Mudigere", "Narasimharajapura", "Sringeri", "Tarikere"],
        "CHITRADURGA": ["Challakere", "Chitradurga", "Hiriyur", "Holalkere", "Hosdurga", "Molakalmuru"],
        "DAKSHINA KANNADA": ["Bantval", "Beltangadi", "KADABA", "MOODUBIDIRE", "Mangaluru", "Puttur", "Sulya"],
        "DAVANGERE": ["Channagiri", "Davanagere", "Harihar", "Honnali", "Jagalur", "NYAMATHI"],
        "DHARWAD": ["ALNAVAR", "ANNIGERI", "Dharwad", "HUBBALLI URBAN", "Hubballi", "Kalghatgi", "Kundgol", "Navalgund"],
        "GADAG": ["GAJENDRAGAD", "Gadag", "LAXMESHWAR", "Mundargi", "Nargund", "Ron", "Shirhatti"],
        "HASSAN": ["Alur", "Arkalgud", "Arsikere", "Belur", "Channarayapatna", "Hassan", "Hole Narsipur", "Sakleshpur"],
        "HAVERI": ["Byadgi", "Hangal", "Haveri", "Hirekerur", "RATTIHALLI", "Ranibennur", "Savanur", "Shiggaon"],
        "KALABURAGI": ["Afzalpur", "Aland", "Chincholi", "Chittapur", "Jevargi", "KALAGI", "KAMALAPUR", "Kalaburagi", "SHAHABAD", "Sedam", "YADRAMI"],
        "KODAGU": ["KUSHALANAGAR", "Madikeri", "PONNAMPET", "Somvarpet", "Virajpet"],
        "KOLAR": ["Bangarapet", "KOLAR GOLD FIELD", "Kolar", "Malur", "Mulbagal", "Srinivaspur"],
        "KOPPAL": ["Gangawati", "KANAKAGIRI", "KARATAGI", "KUKUNOOR", "Koppal", "Kushtagi", "Yelbarga"],
        "MANDYA": ["Krishnarajpet", "Maddur", "Malavalli", "Mandya", "Nagamangala", "Pandavapura", "Shrirangapattana"],
        "MYSURU": ["Heggadadevankote", "Hunsur", "Krishnarajanagara", "Mysuru", "Nanjangud", "Piriyapatna", "SARAGURU", "Tirumakudal - Narsipur"],
        "RAICHUR": ["Devadurga", "Lingsugur", "MASKI", "Manvi", "Raichur", "SIRWAR", "Sindhnur"],
        "RAMANAGARA": ["Channapatna", "Kanakapura", "Magadi", "Ramanagara"],
        "SHIVAMOGGA": ["Bhadravati", "Hosanagara", "Sagar", "Shikarpur", "Shivamogga", "Sorab", "Tirthahalli"],
        "TUMAKURU": ["Chiknayakanhalli", "Gubbi", "Koratagere", "Kunigal", "Madhugiri", "Pavagada", "Sira", "Tiptur", "Tumakuru", "Turuvekere"],
        "UDUPI": ["BAINDURU", "BRAHMAVARA", "HEBRI", "KAPU", "Karkal", "Kundapura", "Udupi"],
        "UTTARA KANNADA": ["Ankola", "Bhatkal", "DANDELI", "Haliyal", "Honavar", "Karwar", "Kumta", "Mundgod", "Siddapur", "Sirsi", "Supa", "Yellapur"],
        "VIJAYANAGAR": ["Hadagalli", "Hagaribommanahalli", "Harapanahalli", "Hosapete", "KOTTURU", "Kudligi"],
        "VIJAYAPURA": ["ALMEL", "BABALESHWAR", "Basavana Bagevadi", "CHADACHAN", "DEVARA HIPPARAGI", "Indi", "KOLHAR", "Muddebihal", "NIDAGUNDI", "Sindgi", "TALIKOTI", "TIKOTA", "Vijayapura"],
        "YADGIR": ["GURUMITKAL", "HUNASAGI", "Shahpur", "Shorapur", "WADAGERA", "Yadgir"],
    },
    "MADHYA PRADESH": {
        "AGAR MALWA": ["Agar", "Badod", "Nalkheda", "Susner"],
        "ALIRAJPUR": ["Alirajpur", "Bhavra", "Jobat", "Kathiwara", "Sondawa"],
        "ANUPPUR": ["Anuppur", "Jaithari", "Kotma", "Pushparajgarh"],
        "ASHOKNAGAR": ["Ashoknagar", "Bahadurpur", "Chanderi", "Isagarh", "Mungaoli", "Nai Sarai", "Piprai", "Shadhora"],
        "BALAGHAT": ["Baihar", "Balaghat", "Birsa", "Katangi", "Khairlanji", "Kirnapur", "Lalbarra", "Lanji", "Paraswada", "Tirodi", "Waraseoni"],
        "BARWANI": ["Anjad", "Barwani", "Niwali", "Pansemal", "Pati", "Rajpur", "Sendhwa", "Thikri", "Varla"],
        "BETUL": ["Amla", "Athner", "Betul", "Betul Nagar", "Bhainsdehi", "Bhimpur", "Chicholi", "Ghoda Dongri", "Multai", "PrabhatPattan", "Shahpur"],
        "BHIND": ["Ater", "Bhind", "Bhind Nagar", "Gohad", "Gormi", "Lahar", "Mau", "Mehgaon", "Mihona", "Ron"],
        "BHOPAL": ["Berasia", "Huzur", "Kolar"],
        "BURHANPUR": ["Burhanpur", "Burhanpur nagar", "Khaknar", "Nepanagar"],
        "CHHATARPUR": ["Bada Malhera", "Bijawar", "Buxwaha", "Chandla", "Chhatarpur", "Chhatarpur Nagar", "Gaurihar", "Ghuwara", "Laundi", "Maharajpur", "Nowgong", "Rajnagar"],
        "CHHINDWARA": ["Amarwara", "Bichhua", "Chand", "Chaurai", "Chhindwara", "Chhindwara Nagar", "Harrai", "Jamai", "Mohkhed", "Pandhurna", "Parasia", "Sausar", "Tamia", "Umreth"],
        "DAMOH": ["Batiyagarh", "Damoh", "Danyantinagar", "Hatta", "Jabera", "Patera", "Patharia", "Tendukheda"],
        "DATIA": ["Badoni", "Bhander", "Datia", "Datia Nagar", "Indergarh", "Seondha"],
        "DEWAS": ["Bagli", "Dewas", "Dewas Nagar", "Hatpiplya", "Kannod", "Khategaon", "Satwas", "Sonkatch", "Tonk Khurd", "Udainagar"],
        "DHAR": ["Badnawar", "Dahi", "Dhar", "Dharampuri", "Gandhwani", "Kukshi", "Manawar", "Pithampur", "Sardarpur"],
        "DINDORI": ["BAJAG", "Dindori", "Shahpura"],
        "EAST NIMAR": ["Harsud", "Khalwa", "Khandwa", "Khandwa Nagar", "Pandhana", "Punasa"],
        "GUNA": ["Aron", "Bamori", "Chachaura", "Guna", "Guna Nagar", "Kumbhraj", "Maksoodangarh", "Raghogarh"],
        "GWALIOR": ["Bhitarwar", "Chinour", "City center", "Ghatigaon", "Gird", "Murar", "Pichhore Or Dabra", "Tansen"],
        "HARDA": ["Handiya", "Harda", "Khirkiya", "Rehatgaon", "Sirali", "Timarni"],
        "HOSHANGABAD": ["Babai", "Bankhedi", "Dolariya", "Hoshangabad", "Hoshangabad nagar", "Itarsi", "Pipariya", "Seoni-Malwa", "Sohagpur"],
        "INDORE": ["BhicholiHapsi", "Depalpur", "Hatod", "Indore", "Kanadiya", "Khudel", "Malharganj", "Mhow", "Rau", "Sawer"],
        "JABALPUR": ["Adhartal", "Gorakhpur", "Jabalpur", "Kundam", "Majholi", "Panagar", "Patan", "Ranjhi", "Shahpura", "Sihora"],
        "JHABUA": ["Jhabua", "Meghnagar", "Petlawad", "Rama", "Ranapur", "Thandla"],
        "KATNI": ["Badwara", "Bahoriband", "Barhi", "Dhimarkheda", "Katni Nagar", "Murwara or Katni", "Rithi", "Sleemnbad", "Vijayraghavgarh"],
        "KHARGONE": ["Barwaha", "Bhagwanpura", "Bhikangaon", "Gogaon", "Jhiranya", "Kasrawad", "Khargone", "Khargone Nagar", "Maheshwar", "Sanawad", "Segaon"],
        "MANDLA": ["Bichhiya", "Ghughari", "Mandla", "Nainpur", "Narayanganj", "Niwas"],
        "MANDSAUR": ["Bhanpura", "Daloda", "Garoth", "Malhargarh", "Mandsaur", "Mandsaur Nagar", "Shamgarh", "Sitamau", "Suwasara"],
        "MORENA": ["Ambah", "Bamor", "Joura", "Kailaras", "Morena", "Morena Nagar", "Porsa", "Sabalgarh"],
        "NARSINGHPUR": ["Gadarwara", "Gotegaon", "Kareli", "Narsimhapur", "Saikheda", "Tendukheda"],
        "NEEMUCH": ["Jawad", "Jiran", "Manasa", "Neemuch", "Neemuch Nagar", "Rampura", "Singoli"],
        "Niwari": ["Niwari", "Orchha", "Prithvipur"],
        "PANNA": ["Ajaigarh", "Amanganj", "Devendranagar", "Gunnor", "Panna", "Pawai", "Raipura", "Shahnagar", "Simariya"],
        "RAISEN": ["Badi", "Baraily", "Begamganj", "Deori", "Gairatganj", "Goharganj", "Raisen", "Silwani", "Sultanpur", "Udaipura"],
        "RAJGARH": ["Biaora", "Jirapur", "Khilchipur", "Khujner", "Narsinghgarh", "Pachore", "Rajgarh", "Sarangpur", "Suthaliya"],
        "RATLAM": ["Alot", "Bajna", "Jaora", "Piploda", "Ratlam", "Ratlam Nagar", "Rawti", "Sailana", "Tal"],
        "REWA": ["Gurh", "Hanumana", "Huzur", "Huzur nagar", "Jawa", "Mangawan", "Mauganj", "Naigarhi", "Raipur - Karchuliyan", "Semaria", "Sirmour", "Teonthar"],
        "SAGAR": ["Banda", "Bina", "Deori", "Garhakota", "Jaisinagar", "Kesli", "Khurai", "Malthon", "Rahatgarh", "Rehli", "Sagar", "Sagar Nagar", "Shahgarh"],
        "SATNA": ["Amarpatan", "Birsinghpur", "Kotar", "Kothi", "Maihar", "Majhgawan", "Nagod", "Raghurajnagar Nagareey", "Ramnagar", "Rampur Baghelan", "Unchahara"],
        "SEHORE": ["Ashta", "Budni", "Ichhawar", "Jawar", "Nasrullaganj", "Rehti", "Sehore", "Sehore Nagar", "Shyampur"],
        "SEONI": ["Barghat", "Chhapara", "Dhanora", "Ghansaur", "Keolari", "Kurai", "Lakhnadon", "Seoni", "Seoni Nagar"],
        "SHAHDOL": ["Beohari", "Budar", "Gohparu", "Jaisinghnagar", "Jaitpur", "Sohagpur"],
        "SHAJAPUR": ["Awantipur Badodiya", "Gulana", "Kalapipal", "Moman Badodiya", "Polaykala", "Shajapur", "Shujalpur"],
        "SHEOPUR": ["Badoda", "Beerpur", "Karahal", "Sheopur", "Vijaypur"],
        "SHIVPURI": ["Badarwas", "Bairad", "Karera", "Khaniyadhana", "Kolaras", "Narwar", "Pichhore", "Pohri", "Rannod", "Shivpuri", "Shivpuri nagar"],
        "SIDHI": ["Bahari", "Churhat", "Gopadbanas", "Kusmi", "Majhauli", "Rampur Naikin", "Sihawal"],
        "SINGRAULI": ["Chitrangi", "Deosar", "Mada", "Sarai", "Singrauli", "Singrauli Nagar"],
        "TIKAMGARH": ["Badgaon Dhasan", "Baldeogarh", "Jatara", "Khargapur", "Lidhora", "Mohangarh", "Palera", "Tikamgarh"],
        "UJJAIN": ["Badnagar", "Ghatiya", "Jharda", "Khacharod", "Kothi Mahal", "Mahidpur", "Makdon", "Nagda", "Tarana", "Ujjain", "Ujjain Nagar"],
        "UMARIA": ["Bandhogarh", "Bilaspur", "Chandia", "Karkeli", "Manpur", "Nowrozabad", "Pali"],
        "VIDISHA": ["Basoda", "Gulabganj", "Gyaraspur", "Kurwai", "Lateri", "Nateran", "Pathari", "Shamshabad", "Sironj", "Tyonda", "Vidisha", "Vidisha Nagar"],
    },
    "MAHARASHTRA": {
        "AHMEDNAGAR": ["Akola", "Jamkhed", "Karjat", "Kopargaon", "Nagar", "Nevasa", "Parner", "Pathardi", "Rahta", "Rahuri", "Sangamner", "Shevgaon", "Shrigonda", "Shrirampur"],
        "AKOLA": ["Akola", "Akot", "Balapur", "Barshitakli", "Murtijapur", "Patur", "Telhara"],
        "AMRAVATI": ["Achalpur", "Amravati", "Anjangaon Surji", "Bhatkuli", "Chandur Railway", "Chandurbazar", "Chikhaldara", "Daryapur", "Dhamangaon Railway", "Dharni", "Morshi", "Nandgaon-Khandeshwar", "Teosa", "Warud"],
        "AURANGABAD": ["Aurangabad", "Gangapur", "Kannad", "Khuldabad", "Paithan", "Phulambri", "Sillod", "Soegaon", "Vaijapur"],
        "BEED": ["Ambejogai", "Ashti", "Bid", "Dharur", "Georai", "Kaij", "Manjlegaon", "Parli", "Patoda", "Shirur (Kasar)", "Wadwani"],
        "BHANDARA": ["Bhandara", "Lakhandur", "Lakhani", "Mohadi", "Pauni", "Sakoli", "Tumsar"],
        "BULDHANA": ["Buldana", "Chikhli", "Deolgaon Raja", "Jalgaon (Jamod)", "Khamgaon", "Lonar", "Malkapur", "Mehkar", "Motala", "Nandura", "Sangrampur", "Shegaon", "Sindkhed Raja"],
        "CHANDRAPUR": ["Ballarpur", "Bhadravati", "Brahmapuri", "Chandrapur", "Chimur", "Gondpipri", "Jiwati", "Korpana", "Mul", "Nagbhir", "Pombhurna", "Rajura", "Sawali", "Sindewahi", "Warora"],
        "DHULE": ["Dhule", "Sakri", "Shirpur", "Sindkhede"],
        "GADCHIROLI": ["Aheri", "Armori", "Bhamragad", "Chamorshi", "Desaiganj (Vadasa)", "Dhanora", "Etapalli", "Gadchiroli", "Korchi", "Kurkheda", "Mulchera", "Sironcha"],
        "GONDIA": ["Amgaon", "Arjuni Morgaon", "Deori", "Gondiya", "Goregaon", "Sadak-Arjuni", "Salekasa", "Tirora"],
        "HINGOLI": ["Aundha (Nagnath)", "Basmath", "Hingoli", "Kalamnuri", "Sengaon"],
        "JALGAON": ["Amalner", "Bhadgaon", "Bhusawal", "Bodvad", "Chalisgaon", "Chopda", "Dharangaon", "Erandol", "Jalgaon", "Jamner", "Muktainagar (Edlabad)", "Pachora", "Parola", "Raver", "Yawal"],
        "JALNA": ["Ambad", "Badnapur", "Bhokardan", "Ghansawangi", "Jafferabad", "Jalna", "Mantha", "Partur"],
        "KOLHAPUR": ["Ajra", "Bavda", "Bhudargad", "Chandgad", "Gadhinglaj", "Hatkanangle", "Kagal", "Karvir", "Panhala", "Radhanagari", "Shahuwadi", "Shirol"],
        "LATUR": ["Ahmadpur", "Ausa", "Chakur", "Deoni", "Jalkot", "Latur", "Nilanga", "Renapur", "Shirur-Anantpal", "Udgir"],
        "NAGPUR": ["Bhiwapur", "Hingna", "Kalameshwar", "Kamptee", "Katol", "Kuhi", "Mauda", "Nagpur (Rural)", "Nagpur (Urban)", "Narkhed", "Parseoni", "Ramtek", "Savner", "Umred"],
        "NANDED": ["Ardhapur", "Bhokar", "Biloli", "Deglur", "Dharmabad", "Hadgaon", "Himayatnagar", "Kandhar", "Kinwat", "Loha", "Mahoor", "Mudkhed", "Mukhed", "Naigaon (Khairgaon)", "Nanded", "Umri"],
        "NANDURBAR": ["Akkalkuwa", "Akrani", "Nandurbar", "Nawapur", "Shahade", "Talode"],
        "NASHIK": ["Baglan", "Chandvad", "Deola", "Dindori", "Igatpuri", "Kalwan", "Malegaon", "Nandgaon", "Nashik", "Niphad", "Peth", "Sinnar", "Surgana", "Trimbakeshwar", "Yevla"],
        "OSMANABAD": ["Barshi", "Bhum", "Kalamb", "Lohara", "Osmanabad", "Paranda", "Tuljapur", "Umarga", "Washi"],
        "PALGHAR": ["Dahanu", "Jawhar", "Mokhada", "Palghar", "Talasari", "Vada", "Vasai", "Vikramgad"],
        "PARBHANI": ["Gangakhed", "Jintur", "Manwath", "Palam", "Parbhani", "Pathri", "Purna", "Sailu", "Sonpeth"],
        "PUNE": ["Ambegaon", "Baramati", "Bhor", "Daund", "Haveli", "Indapur", "Junnar", "Khed", "Mawal", "Mulshi", "Pune City", "Purandhar", "Shirur", "Velhe"],
        "RAIGAD": ["Alibag", "Karjat", "Khalapur", "Mahad", "Mangaon", "Mhasla", "Murud", "Panvel", "Pen", "Poladpur", "Roha", "Shrivardhan", "Sudhagad", "Tala", "Uran"],
        "RATNAGIRI": ["Chiplun", "Dapoli", "Guhagar", "Khed", "Lanja", "Mandangad", "Rajapur", "Ratnagiri", "Sangameshwar"],
        "SANGLI": ["Atpadi", "Jat", "Kadegaon", "Kavathemahankal", "Khanapur", "Miraj", "Palus", "Shirala", "Tasgaon", "Walwa"],
        "SATARA": ["Jaoli", "Karad", "Khandala", "Khatav", "Koregaon", "Mahabaleshwar", "Man", "Patan", "Phaltan", "Satara", "Wai"],
        "SINDHUDURG": ["Devgad", "Dodamarg", "Kankavli", "Kudal", "Malwan", "Sawantwadi", "Vaibhavvadi", "Vengurla"],
        "SOLAPUR": ["Akkalkot", "Barshi", "Karmala", "Madha", "Malshiras", "Mangalvedhe", "Mohol", "Pandharpur", "Sangole", "Solapur North", "Solapur South"],
        "THANE": ["Ambarnath", "Bhiwandi", "Kalyan", "Murbad", "Shahapur", "Thane", "Ulhasnagar"],
        "WARDHA": ["Arvi", "Ashti", "Deoli", "Hinganghat", "Karanja", "Samudrapur", "Seloo", "Wardha"],
        "WASHIM": ["Karanja", "Malegaon", "Mangrulpir", "Manora", "Risod", "Washim"],
        "YAVATMAL": ["Arni", "Babulgaon", "Darwha", "Digras", "Ghatanji", "Kalamb", "Kelapur", "Mahagaon", "Maregaon", "Ner", "Pusad", "Ralegaon", "Umarkhed", "Wani", "Yavatmal", "Zari-Jamani"],
    },
}

# ================================================================
# STATE → VALID PIN CODE RANGES
# ================================================================
STATE_PIN_RANGES = {
    "ANDHRA PRADESH": (500000, 535999),
    "GUJARAT":        (360000, 396999),
    "KARNATAKA":      (560000, 591999),
    "MADHYA PRADESH": (450000, 488999),
    "MAHARASHTRA":    (400000, 445999),
}


def _get_random_address():
    """Pick a valid state → district → taluka + matching pin code from ADDRESS_DATA."""
    state = random.choice(list(ADDRESS_DATA.keys()))
    district = random.choice(list(ADDRESS_DATA[state].keys()))
    taluka = random.choice(ADDRESS_DATA[state][district])
    pin_start, pin_end = STATE_PIN_RANGES.get(state, (400000, 499999))
    pin_code = str(random.randint(pin_start, pin_end))
    return state, district, taluka, pin_code


# ================================================================
# 1. SINGLE COMPANY — generates unique data every time
# ================================================================

def _generate_single_company():
    """
    Generate a unique SINGLE_COMPANY dict each time it's called.
    Uses UUID suffix + timestamp to guarantee uniqueness across runs.
    """
    uid = uuid.uuid4().hex[:4].upper()
    ts = datetime.now().strftime("%H%M%S")

    prefix = random.choice(["Apex", "Zenith", "Nova", "Pulse", "Vertex", "Orion"])
    suffix = random.choice(["Technologies", "Solutions", "Services", "Systems", "Enterprises"])
    middle = random.choice(["Global", "Prime", "Digital", "Smart", "Green", "Royal", "Elite", "Max", "Core", "Link"])
    company_name = f"{prefix} {middle} {suffix}"

    first = random.choice(["Aarav", "Vedant", "Arjun", "Rohan", "Nikhil", "Priya", "Sneha"])
    last = random.choice(["Sharma", "Patil", "Desai", "Joshi", "Kulkarni", "Mehta", "Pawar"])

    pan_prefix = "".join(random.choices(string.ascii_uppercase, k=5))
    pan_digits = "".join(random.choices(string.digits, k=4))
    pan = f"{pan_prefix}{pan_digits}F"

    cin_random = "".join(random.choices(string.digits, k=5))
    cin_year = random.choice(["2020", "2021", "2022", "2023", "2024", "2025"])
    cin_num = "".join(random.choices(string.digits, k=6))
    cin = f"U{cin_random}MH{cin_year}PTC{cin_num}"

    gst_state = random.choice(["27", "29", "33", "24", "08"])
    gstin = f"{gst_state}{pan_prefix[:5]}{pan_digits}A1Z5"

    tan_city = random.choice(["PUNE", "MUM", "BLR", "CHE", "DEL", "HYD"])
    tan_num = "".join(random.choices(string.digits, k=5))
    tan = f"{tan_city}{tan_num}A"

    mobile = f"9{random.randint(100000000, 999999999)}"

    # BUG FIX 1: unpack 4 values (state, district, taluka, pin_code)
    state, district, taluka, pin_code = _get_random_address()


    return {
        "company_name": company_name,
        "entity_group": "FPC",
        "parent_name": "Agdi",
        "company_linked": ["Agdi"],
        "company_short_name": f"{prefix[:3]}{middle[:3]}{suffix[:3]}",
        "contact_name": f"{first} {last}",
        "company_background": "Software development and IT consulting services",
        "email": f"{first.lower()}.{last.lower()}{uid}@testmail.com",
        "mobile_number": mobile,
        "pan": pan,
        "tan": tan,
        "gstin": gstin,
        "cin": cin,
        "is_2fa": False,
        "address_type": "Registered Address",
        "country": "India",
        "state": state,
        "district": district,
        "taluka": taluka,
        "address": f"{uid}, Test Street, {taluka}",
        # BUG FIX 2: use pin_code from _get_random_address() instead of hardcoded range
        "pin_code": pin_code,
        "promoters": random.sample(PROMOTER_DATA, 2),
        "business_model": BUSINESS_MODEL,
        "market_linkages": MARKET_LINKAGES,
        "line_of_business": LINE_OF_BUSINESS,
        "additional_business_activities": ADDITIONAL_BUSINESS_ACTIVITIES,
        "infra_location": random.choice(INFRASTRUCTURE_LOCATIONS),
            "num_addresses": 2,
            "num_business_rows": 2,
            "num_infra_rows": 2,
            "num_addresses": 2,
            "num_business_rows": 2,
            "num_infra_rows": 2
    }


# Call it once at import time — unique every run
SINGLE_COMPANY = _generate_single_company()


# ================================================================
# 2. LOOKUP TABLES
# ================================================================

COMPANY_PREFIXES = [
    "Apex", "Zenith", "Nova", "Pulse", "Vertex", "Orion", "Nexus", "Prism",
    "Crest", "Forge", "Ember", "Atlas", "Solaris", "Quantum", "Helix", "Titan",
    "Cobalt", "Sterling", "Radiant", "Catalyst", "Pinnacle", "Vanguard", "Echo",
    "Matrix", "Vector", "Horizon", "Summit", "Cedar", "Flux", "Aether", "Lunar",
    "Sapphire", "Emerald", "Ruby", "Opal", "Topaz", "Jade", "Amber", "Onyx",
    "Ivory", "Coral", "Scarlet", "Azure", "Indigo", "Violet", "Crimson", "Magenta",
]

COMPANY_SUFFIXES = [
    "Technologies", "Industries", "Enterprises", "Solutions", "Systems",
    "Services", "Corporation", "Holdings", "Group", "Ventures",
    "Analytics", "Innovations", "Dynamics", "Networks", "Infra",
    "Logistics", "Trading", "Manufacturing", "Consulting", "Works",
    "Global", "India", "Prime", "One", "Pro", "Lab", "Tech", "Soft",
]

COMPANY_MIDDLE_WORDS = [
    "Global", "Prime", "East", "West", "North", "South", "Central",
    "Digital", "Smart", "Green", "Royal", "Golden", "Elite", "Premium",
    "Supreme", "Ultra", "Max", "Pro", "Core", "Link",
]

ENTITY_GROUP_OPTIONS = ["FPC"]
PARENT_NAME_OPTIONS = ["Agdi"]
COMPANY_LINKED_OPTIONS = [["Agdi"]]

CONTACT_FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vedant", "Arjun", "Sai", "Rohan",
    "Amit", "Nikhil", "Prashant", "Suresh", "Mahesh", "Rajesh",
    "Priya", "Pooja", "Sneha", "Neha", "Anita", "Kavita", "Swati",
    "Ajay", "Vijay", "Manoj", "Deepak", "Sanjay", "Rakesh", "Mukesh",
]

CONTACT_LAST_NAMES = [
    "Sharma", "Patil", "Desai", "Joshi", "Kulkarni", "Mehta", "Shah",
    "Pawar", "Jadhav", "Chavan", "Bhosale", "More", "Kale", "Gaikwad",
    "Mishra", "Gupta", "Verma", "Singh", "Reddy", "Nair",
]

COUNTRY_OPTIONS = ["India"]


# ================================================================
# 3. BULK DATA GENERATOR
# ================================================================

def generate_bulk_companies(count=1000, start_index=1):
    """
    Generate a list of unique company data dicts.

    Args:
        count:       Number of companies to generate (default: 1000)
        start_index: Starting index for naming (default: 1)
    """
    companies = []

    for i in range(start_index, start_index + count):
        idx = i
        uid_suffix = uuid.uuid4().hex[:6].upper()

        prefix = random.choice(COMPANY_PREFIXES)
        middle = random.choice(COMPANY_MIDDLE_WORDS)
        background = random.choice(COMPANY_BACKGROUNDS)
        suffix = random.choice(COMPANY_SUFFIXES)
        company_name = f"{prefix} {middle} {suffix}"

        short_name = f"{prefix[:3]}{middle[:3]}{suffix[:3]}"

        first_name = random.choice(CONTACT_FIRST_NAMES)
        last_name = random.choice(CONTACT_LAST_NAMES)
        contact_name = f"{first_name} {last_name}"

        email_user = f"{first_name.lower()}.{last_name.lower()}{idx}"
        email_domains = ["company.com", "corp.in", "enterprise.in", "testmail.com"]
        email = f"{email_user}@{random.choice(email_domains)}"

        mobile = f"9{random.randint(100000000, 999999999)}"

        pan_prefix = "".join(random.choices(string.ascii_uppercase, k=5))
        pan_digits = f"{idx:04d}"[-4:]
        pan = f"{pan_prefix}{pan_digits}F"

        cin_random = "".join(random.choices(string.digits, k=5))
        cin_year = random.choice(["2020", "2021", "2022", "2023", "2024", "2025"])
        cin_num = f"{idx:06d}"
        cin = f"U{cin_random}MH{cin_year}PTC{cin_num}"

        gst_state_code = random.choice(["27", "29", "33", "24", "08"])
        gst_pan_part = pan_prefix[:5] + pan_digits
        gstin = f"{gst_state_code}{gst_pan_part}A1Z5"

        tan_city = random.choice(["PUNE", "MUM", "BLR", "CHE", "DEL", "HYD", "KOL", "AHM"])
        tan_num = "".join(random.choices(string.digits, k=5))
        tan = f"{tan_city}{tan_num}A"

        entity_group = random.choice(ENTITY_GROUP_OPTIONS)
        parent_name = random.choice(PARENT_NAME_OPTIONS)
        company_linked = random.choice(COMPANY_LINKED_OPTIONS)

        # BUG FIX 3: unpack 4 values and use the returned pin_code
        state, district, taluka, pin_code = _get_random_address()

        address_line = f"{idx}, Test Street, {taluka}"

        # pin_code already set from _get_random_address() — no override needed

        company = {
            "company_name": company_name,
            "entity_group": entity_group,
            "parent_name": parent_name,
            "company_linked": company_linked,
            "company_short_name": short_name,
            "contact_name": contact_name,
            "company_background": background,
            "email": email,
            "mobile_number": mobile,
            "pan": pan,
            "tan": tan,
            "gstin": gstin,
            "cin": cin,
            "plan_type": "",
            "is_2fa": False,
            "address_type": "Registered Address",
            "country": "India",
            "state": state,
            "district": district,
            "taluka": taluka,
            "address": address_line,
            "pin_code": pin_code,
        "promoters": random.sample(PROMOTER_DATA, 2),
            "business_model": BUSINESS_MODEL,
            "market_linkages": MARKET_LINKAGES,
            "line_of_business": LINE_OF_BUSINESS,
            "additional_business_activities": ADDITIONAL_BUSINESS_ACTIVITIES,
            "infra_location": random.choice(INFRASTRUCTURE_LOCATIONS)
        }

        companies.append(company)

    return companies


# ================================================================
# 4. UTILITY — EXPORT TO EXCEL / CSV
# ================================================================

def save_bulk_data_to_excel(companies, filepath="bulk_companies.xlsx"):
    try:
        import pandas as pd
        df = pd.DataFrame(companies)
        for col in ["business_type", "business_model", "company_linked"]:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
        df.to_excel(filepath, index=False, engine="openpyxl")
        print(f"Saved {len(companies)} companies to: {filepath}")
        return True
    except ImportError:
        print("ERROR: pandas and openpyxl are required. Install with: pip install pandas openpyxl")
        return False


def save_bulk_data_to_csv(companies, filepath="bulk_companies.csv"):
    try:
        import csv

        if not companies:
            print("No data to save")
            return False

        flat_companies = []
        for c in companies:
            row = {}
            for k, v in c.items():
                if isinstance(v, list):
                    row[k] = ", ".join(v)
                else:
                    row[k] = v
            flat_companies.append(row)

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=flat_companies[0].keys())
            writer.writeheader()
            writer.writerows(flat_companies)

        print(f"Saved {len(companies)} companies to: {filepath}")
        return True
    except Exception as e:
        print(f"Error saving CSV: {e}")
        return False


def load_bulk_data_from_excel(filepath):
    try:
        import pandas as pd

        df = pd.read_excel(filepath, engine="openpyxl")
        companies = df.to_dict("records")

        for company in companies:
            for field in ["business_type", "business_model", "company_linked"]:
                if field in company and isinstance(company[field], str):
                    company[field] = [
                        item.strip() for item in company[field].split(",") if item.strip()
                    ]

        print(f"Loaded {len(companies)} companies from: {filepath}")
        return companies
    except ImportError:
        print("ERROR: pandas and openpyxl are required")
        return []
    except Exception as e:
        print(f"Error loading Excel: {e}")
        return []


# ================================================================
# 5. QUICK STANDALONE TEST
# ================================================================

if __name__ == "__main__":
    print("=" * 60)
    print(" COMPANY ONBOARDING DATA GENERATOR")
    print("=" * 60)

    print("\n[SINGLE COMPANY TEMPLATE]")
    print("-" * 40)
    for key, value in SINGLE_COMPANY.items():
        if isinstance(value, list):
            print(f"  {key:25s}: {', '.join(value)}")
        else:
            print(f"  {key:25s}: {value}")

    print("\n[BULK GENERATION — 5 SAMPLE]")
    print("-" * 40)
    samples = generate_bulk_companies(5)
    for i, company in enumerate(samples, 1):
        print(f"\n  Company {i}:")
        print(f"    Name         : {company['company_name']}")
        print(f"    Entity Group : {company['entity_group']}")
        print(f"    Parent Name  : {company['parent_name']}")
        print(f"    Company Linked: {company['company_linked']}")
        print(f"    Email        : {company['email']}")
        print(f"    PAN          : {company['pan']}")
        print(f"    CIN          : {company['cin']}")
        print(f"    State        : {company['state']}")
        print(f"    District     : {company['district']}")
        print(f"    Taluka       : {company['taluka']}")
        print(f"    Pin Code     : {company['pin_code']}")

    print("\n[GENERATING 1000 COMPANIES]")
    print("-" * 40)
    thousand = generate_bulk_companies(1000)
    print(f"  Generated: {len(thousand)} companies")
    print(f"  First name: {thousand[0]['company_name']}")
    print(f"  Last name : {thousand[-1]['company_name']}")

    names = [c["company_name"] for c in thousand]
    pans = [c["pan"] for c in thousand]
    cins = [c["cin"] for c in thousand]
    print(f"  Unique names: {len(set(names))}/{len(names)}")
    print(f"  Unique PANs : {len(set(pans))}/{len(pans)}")
    print(f"  Unique CINs : {len(set(cins))}/{len(cins)}")

    print("\n" + "=" * 60)
    print(" DONE — Run this file standalone to test data generation")
    print("=" * 60)
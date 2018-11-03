import re
import orodja

# URL glavne strani z nepremičninami
# 'https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/'

# mapa, v katero bomo shranili zajete strani
# 'zajete-strani'

# mapa, v katero bomo shranili podatke
# 'obdelani-podatki'

# ime CSV datoteke v katero bomo shranili podatke
# 'stanovanja.csv'

# najprej shranim vse spletne strani z oglasi
# dne 23.10.2018, 59 strani
# (od 1 do 59, vse skupaj 1768 zadetkov)

for i in range(1, 60):
    url = (
        'https://www.nepremicnine.net/'
        'oglasi-prodaja/'
        'ljubljana-mesto/stanovanje/{}/'
    ).format(i)
    orodja.shrani_spletno_stran(
        url, 'zajete_strani/stanovanja_ljubljana_{}.html'.format(i)
    )

# sestavimo regularani izraz, ki poišče vse bloke oglasov

vzorec_bloka = re.compile(
    r'<div class="oglas_container'
    r'.*?'
    r'<div class="clearer"></div>',
    re.DOTALL)

# sestavim regularni izraz za podatke, ki jih želim pridobiti iz oglasa

vzorec_oglasa = re.compile(
    r'id="(?P<id>\d+?)"'
    r'.*?'
    r'class="tipi">(?P<tip>\w*?)</span></span>'
    r'.*?'
    r'<span\s?class="atribut'
    r'(">Nadstropje:\s<strong>(?P<nadstropje>\w*?)</strong>)?'
    r'.*?'
    r'leto">Leto:\s<strong>(?P<leto>\d*)'
    r'.*?'
    r'itemprop="description">(?P<opis>.*?)</div>'
    r'.*?'
    r'class="velikost">(?P<velikost>.*?)\sm2'
    r'.*?'
    r'class="cena">(?P<cena>.*?)\s\&euro'
    r'.*?'
    r'class="agencija">(?P<agencija>.*?)</span>',
    re.DOTALL)

# sestavim regularni izraz, ki bo iz naslova oglasa ugotovil upravno enoto

vzorec_enota = re.compile(
    r'class="title">(?P<enota>.*?)</span></a></h2>',
    flags=re.DOTALL
)

# sestavim regularni izraz, ki bo iz kratkega opisa ugotovil,
# kdaj je bilo stanovanje adaptirano

vzorec_adaptacija = re.compile(
    r'.*?'
    r'adaptiran\w*?\sl\.\s(?P<adaptirano>\d{4})',
    flags=re.DOTALL
)


# napišem fukncijo, ki bo izločila podatke iz bloka oglasa

def izloci_podatke_oglasa(blok):
    ''' Iz bloka oglasa izloči vse iskane podatke in jih spravi v slovar.'''
    oglas = {}
    ujemanje = vzorec_oglasa.search(blok)
    if ujemanje is not None:
        oglas = ujemanje.groupdict()

        oglas['id'] = int(oglas['id'])
        oglas['tip'] = str(oglas['tip'])
        oglas['nadstropje'] = str(oglas['nadstropje'])
        oglas['leto'] = int(oglas['leto'])
        oglas['opis'] = str(oglas['opis']).replace('&quot;', '')
        oglas['velikost'] = float(oglas['velikost'].replace(',', '.'))
        oglas['cena'] = float(oglas['cena'].replace('.', '').replace(',', '.'))
        oglas['agencija'] = str(oglas['agencija'])

        # dodamo upravno enoto iz naslova
        ujemanje = vzorec_enota.search(blok)
        if ujemanje:
            oglas['enota'] = str(ujemanje['enota']).split(',')[0]
        else:
            oglas['enota'] = None

        # dodamo leto adptacije, če je bila zgradba adaptirana
        ujemanje1 = vzorec_adaptacija.search(oglas['opis'])
        if ujemanje1:
            oglas['adaptirano'] = int(ujemanje1['adaptirano'])
        else:
            oglas['adaptirano'] = None

    return oglas


# napišem funkcijo, ki bo iz zajete spletne strani poiskala bloke
# in na teh blokih uporabila funkcijo 'izloci_podatke_oglasa'

def stanovanja_na_strani(st_strani):
    ime_datoteke = 'zajete_strani/stanovanja_ljubljana_{}.html'.format(
        st_strani)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    for blok in vzorec_bloka.finditer(vsebina):
        yield izloci_podatke_oglasa(blok.group(0))


# napišem for zanko, ki uporabi funkcijo stanovanje_na_strani na vsaki
# spletni strani in slovar s podatki oglasa doda v seznam oglasi

oglasi = []
for st_strani in range(1, 60):
    for oglas in stanovanja_na_strani(st_strani):
        if oglas != {}:
            oglasi.append(oglas)

# v seznamu oglasi imam sedaj vse slovarje, ki predstavljajo posamezni oglas

# vsak slovar vsebuje ključe:
# id, tip, nadstropje, leto, opis, velikost, cena, agencija, enota, adaptirano

# zapišem sedaj podatke v csv in razvrstim stolpce


orodja.zapisi_csv(
    oglasi,
    ['id', 'enota', 'tip', 'leto', 'adaptirano', 'nadstropje',
     'velikost', 'cena', 'agencija', 'opis'],
    'obdelani-podatki/stanovanja.csv'
)

# zapišem še v json datoteki za pregled

orodja.zapisi_json(oglasi, 'obdelani-podatki/stanovanja.json')

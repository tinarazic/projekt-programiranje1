import csv
import json
import os
import re
import sys
import requests
import orodja

# URL glavne strani z nepremičninami
# 'https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/'

# mapa, v katero bomo shranili podatke
# obdelani-podatki'

# ime CSV datoteke v katero bomo shranili podatke
# 'stanovanja.csv'

# najprej shranim vse strani dne 23.10.2018 (od 1 do 59, vse skupaj 1768 zadetkov)

for i in range(1, 60):
    url = (
        'https://www.nepremicnine.net/'
        'oglasi-prodaja/'
        'ljubljana-mesto/stanovanje/{}/'
    ).format(i)
    orodja.shrani_spletno_stran(
        url, 'zajete_strani/stanovanja_ljubljana_{}.html'.format(i)
    )

# sestavimo vzorec, ki poišče vse bloke oglasov

vzorec_bloka = re.compile(
    r'<div class="oglas_container'
    r'.*?'
    r'<div class="clearer"></div>',
    re.DOTALL)

# sestavimo vzorce za podatke, ki jih želimo

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

vzorec_enota = re.compile(
    r'class="title">(?P<enota>.*?)</span></a></h2>',
    flags=re.DOTALL
)

vzorec_adaptacija = re.compile(
    r'.*?'
    r'adaptiran\w*?\sl\.\s(?P<adaptirano>\d{4})',
    flags=re.DOTALL
)

# poiščemo vse bloke oglasov na spletni strani

def stanovanja_na_strani(st_strani):
    ime_datoteke = 'zajete_strani/stanovanja_ljubljana_{}.html'.format(
        st_strani)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    for blok in vzorec_bloka.findall(vsebina):
        yield blok

# shranimo vse bloke oglasov iz vseh strani v seznam oglasi

oglasi = []
for st_strani in range(1, 60):
    for blok in stanovanja_na_strani(st_strani):
        oglasi.append(blok)

# v seznamu oglasi imamo sedaj vse bloke iz vseh strani

# naredimo seznam slovarjev in uredimo podatke

slovarji = []

for blok in oglasi:
    for ujemanje in vzorec_oglasa.finditer(blok):
        oglas = ujemanje.groupdict()

        oglas['id'] = int(oglas['id'])
        oglas['tip'] = str(oglas['tip'])
        oglas['nadstropje'] = str(oglas['nadstropje'])
        oglas['leto'] = int(oglas['leto'])
        oglas['opis'] = str(oglas['opis'])
        oglas['velikost'] = float(oglas['velikost'].replace(',', '.'))
        oglas['cena'] = float(oglas['cena'].replace('.', '').replace(',', '.'))
        oglas['agencija'] = str(oglas['agencija'])

        # dodamo upravno enoto iz naslova
        ujemanje = vzorec_enota.search(blok)
        if ujemanje:
            oglas['enota'] = str(ujemanje['enota']).split(',')[0]
        else:
            oglas['enota'] = "None"

        # dodamo leto adptacije, če je bila zgradba adaptirana
        ujemanje1 = vzorec_adaptacija.search(oglas['opis'])
        if ujemanje1:
            oglas['adaptirano'] = int(ujemanje1['adaptirano'])
        else:
            oglas['adaptirano'] = 'None'

        slovarji.append(oglas)

# vsak slovar vsebuje ključe:
# id, tip, nadstropje, leto, opis, velikost, cena, agencija, enota, adaptirano

# zapišimo sedaj podatke v csv (in json za vpogled) in razvrstimo stolpce

orodja.zapisi_csv(
    slovarji,
    ['id', 'enota', 'tip', 'leto', 'adaptirano', 'nadstropje', 'velikost', 'cena', 'agencija', 'opis'],
    'obdelani-podatki/stanovanja.csv'
)
orodja.zapisi_json(slovarji, 'obdelani-podatki/stanovanja.json')

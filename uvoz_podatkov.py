import csv
import json
import os
import re
import sys
import requests
import orodja

# definiramo URL glavne strani z nepremičninami
nepremicnine_frontpage_url = 'https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/'
# mapa, v katero bomo shranili podatke
nepremicnine_directory = '_podatki'
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'nepremicnine.html'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'stanovanja.csv'

# shranim vse strani dne 23.10.2018 (od 1 do 59, vse skupaj 1768 zadetkov)

for i in range(1, 60):
    url = (
        'https://www.nepremicnine.net/'
        'oglasi-prodaja/'
        'ljubljana-mesto/stanovanje/{}/'
    ).format(i)
    orodja.shrani_spletno_stran(url, 'zajete_strani/stanovanja_ljubljana_{}.html'.format(i))

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
    r'.*?<span\s?class="atribut'
    r'(">Nadstropje:\s<strong>(?P<nadstropje>\w*?)</strong>)?.*?'
    r'leto">Leto:\s<strong>(?P<leto>\d*)'
    r'.*?'
    r'itemprop="description">(?P<opis>.*?)</div>'
    r'.*?'
    #r'class="velikost">(?P<velikost>\w*?)</span><br\s/>'
    #r'.*?'
    #r'class="cena">(?P<cena>\w*?)</span>'
    #r'.*?'
    #r'class="agencija">(?P<agencija>\w*?)</span>'
    r'.*?',
    re.DOTALL)

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
    for oglas in stanovanja_na_strani(st_strani):
        oglasi.append(oglas)

# v seznamu oglasi imamo sedaj vse bloke iz vseh strani

slovarji = []

for blok in oglasi:
    for ujemanje in vzorec_oglasa.finditer(blok):
        oglas = ujemanje.groupdict()
        slovarji.append(oglas)

orodja.zapisi_csv(slovarji, ['id', 'tip', 'nadstropje', 'leto', 'velikost', 'opis'], 'obdelani-podatki/stanovanja.csv')
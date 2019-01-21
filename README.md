# Analiza ponudbe stanovanj v Ljubljani

V svoji projektni nalogi sem analizirala ponudbo stanovanj v Ljubljani.

## Pridobivanje podatkov

Tabela o ponudbi stanovanj se nahaja v *obdelani_podatki/stanovanja.csv*. Podatke sem pridobila s spletne strani https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/. Regularni izrazi in koda, s katero sem pridobila podatke, so zapisani v datoteki *uvoz_podatkov.py*.

Za vsako stanovanje sem pridobila naslednje podatke:
- id stanovanja,
- območje
- tip stanovanja,
- leto gradnje,
- leto adaptacije,
- nadstropje,
- velikost stanovanja,
- ceno,
- agencijo, ki stanovanje ponuja,
- kratek opis stanovanja.

## Hipoteze

S pomočjo urejenih podatkov sem poskušala analizirati:
- na katerih območjih je ponudba največja?
- kje so najdražja/najcenejša stanovanja?
- ali leto gradnje vpliva na ceno?
- ali se cena stanovanja res povečuje z velikostjo?
- ali so adaptirana stanovanja dražja?
- katera agencija ima v lasti največ ponudb?
...

Rezultati moje analize so predstavljeni v datoteki **_Analiza ponudbe stanovanj v Ljubljani.ipynb_**.




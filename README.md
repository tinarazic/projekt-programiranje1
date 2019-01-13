# Analiza ponudbe stanovanj v Ljubljani

V svoji projektni nalogi sem analizirala ponudbo stanovanj v Ljubljani.

## Pridobivanje podatkov

Tabela o ponudbi stanovanj se nahaja v *obdelani_podatki/stanovanja.csv*. Podatke sem pridobila s spletne strani https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/. Regularni izrazi in koda, s katero sem pridobila podatke, so zapisani v datoteki *uvoz_podatkov.py*.

Za vsako stanovanje sem pridobila naslednje podatke:
- id stanovanja,
- upravno enoto, v kateri se stanovanje nahaja,
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
- v katerih upravnih enotah je ponudba največja?
- ali se prodaja več stanovanj v blokih ali v hišah?
- ali leto gradnje vpliva na ceno?
- ali se cena stanovanja res povečuje z velikostjo?
- kje so najdražja stanovanja?
- katera agencija ima v lasti največ ponudb?
...

Rezultati moje analize so predstavljeni v datoteki **Analiza ponudbe stanovanj v Ljubljani.ipynb**.




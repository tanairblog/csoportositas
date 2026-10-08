# 3D Ízléstérkép

Interaktív 3D vizualizációs eszköz zenei preferenciák feltérképezésére főkomponens-elemzés (PCA) és a Plotly könyvtár segítségével.

A script mind a tételeket (dalok, videók), mind az értékelőket (diákok, résztvevők) egyetlen közös 3D koordinátarendszerbe vetíti:
* **Dalok:** pontokként jelennek meg a térben; azok a számok alkotnak csoportokat, amelyeket a résztvevők hasonlóan értékeltek.
* **Értékelők:** a középpontból kiinduló irányvektorokként (nyilakként) láthatók; a vektor abba az irányba mutat, amerre az adott személy által legjobbra értékelt dalok találhatók.

---

## Főbb funkciók

* **Közös 3D tér (PCA Biplot):** Egyszerre ábrázolja a dalokat és a diákok ízlését.
* **Pontozási torzítás kiszűrése:** Az értékeléseket automatikusan személyes z-értékekké standardizálja ($z = \frac{x - \mu}{\sigma}$), így a szigorúbb és a megengedőbb pontozási szokások nem torzítják el a távolságokat.
* **Hiányzó értékek kezelése:** Ha a résztvevők üresen hagyták a saját beküldött daluk értékelését, a script automatikusan 10.0 értékkel helyettesíti a hiányzó cellákat.
* **Önálló, interaktív kimenet:** Egyetlen önálló `.html` fájlt generál, amely bármely modern böngészőben megnyitható, szabadon forgatható, nagyítható, és az elemek fölé vive a kurzort megjeleníti a pontos címeket és neveket.

---

## Rendszerkövetelmények

A futtatáshoz legalább Python 3.8 verzió szükséges. A függőségek telepítése terminálból:

```bash
pip install pandas numpy scikit-learn plotly openpyxl

```

---

## Az adatok előkészítése

A script `.csv` és `.xlsx` formátumú táblázatokat is kezel. A táblázat szerkezete a következő legyen:

1. Az **első oszlop** tartalmazza a dalok vagy videók címeit.
2. A **további oszlopok** a résztvevők (diákok) neveit tartalmazzák.
3. A **cellákban** a leadott pontszámok szerepeljenek (pl. 1–10 skálán).

### Példa (`ratings.csv`):

```csv
Song,Anna,Bence,Csilla,Dániel
Bohemian Rhapsody,10,7,10,8
Blinding Lights,6,10,5,9
Smells Like Teen Spirit,9,8,10,7
Take On Me,7,6,8,10

```

> **Megjegyzés a saját dalokhoz:** Ha valaki üresen hagyta a saját maga által beküldött videó sorát, a script az üres (NaN) mezőket automatikusan `10.0` értékkel tölti fel.

---

## Használat

1. Helyezd el a `music_map.py` fájlt és a táblázatot ugyanabban a könyvtárban.
2. Nyisd meg a `music_map.py` fájlt, és ellenőrizd, hogy a `DATA_FILE` változó a megfelelő fájlra mutat-e:
```python
DATA_FILE = "ratings.csv"  # vagy "ratings.xlsx"

```


3. Futtasd a scriptet terminálból:
```bash
python music_map.py

```


4. A futás végén a script létrehozza a `music_landscape_3d.html` fájlt, és automatikusan megnyitja az alapértelmezett böngészőben.

---

## Az ábra értelmezése

* **Dalok közötti távolság:** Azok a számok, amelyek közel esnek egymáshoz a 3D térben, műfajtól függetlenül azonos megítélést kaptak a csoporttól (ugyanazok szerették vagy nem szerették őket).
* **Diákvektor iránya:** A piros nyíl abba az irányba mutat, ahol az adott diák saját átlagához képest a leginkább kedvelt dalai tömörülnek.
* **Ellentétes vektorok:** Ha két diák nyila megközelítőleg ellentétes irányba ($180^\circ$) mutat, az ízlésük a csoport fő törésvonalai mentén markánsan eltér egymástól.
* **Vektor hossza:** A hosszabb nyíl olyan diákot jelöl, akinek az ízlése szorosan illeszkedik a csoport általános fő irányaihoz (PC1, PC2, PC3). A középponthoz közeli, rövid nyíl olyan résztvevőt jelez, akinek a preferenciái egyediek, eklektikusak, és kívül esnek a közösség főbb mintázatain.
* **A pontfelhő közepe:** A koordinátarendszer középpontjához $(0, 0, 0)$ közel elhelyezkedő dalok általában a „konszenzusos”, átlagos pontszámot kapott, kevésbé megosztó tételek.

```

```

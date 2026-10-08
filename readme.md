# 3D ízléstérkép

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

## Hogyan csinálja?

A háttérben zajló folyamat négy matematikai lépésre épül:

**1. A személyes pontozási stílus kisimítása (standardizálás)**

Mindenki másképp skáláz: van, akinél a 7-es már lelkes dicséret, más szinte mindenkinek 9-et vagy 10-et ad. A számítás ezért nem a nyers pontszámokat nézi, hanem azt, hogy egy adott dal mennyivel tér el az illető saját átlagától (z-score). Ezzel a szigorú és a megengedő értékelők ugyanarra a közös skálára kerülnek.

**2. A hasonlóság mérése (korreláció mint távolság)**

Két dal akkor kerül közel egymáshoz, ha a csoport tagjai hasonlóan reagáltak rájuk: ugyanazok emelték ki vagy húzták le őket. A standardizált értékek közötti geometriai távolság pontosan a statisztikai korrelációnak felel meg. Nem az számít, hogy hány pontot kapott a szám, hanem az, hogy kiknek az ízlése mozgott együtt a megítélésekor.

**3. Vetítés 3D térbe (főkomponens-elemzés / PCA)**

Ha 20 diák pontozott, a dalok valójában egy 20 dimenziós térben lebegnek, ahol minden diák véleménye egy külön tengely. Ezt emberi szemmel lehetetlen átlátni. A PCA algoritmus megkeresi azt a 3 legfontosabb fő irányt (a véleménykülönbségek három legerősebb törésvonalát), amelyek a csoport ízlésbeli varianciájának legnagyobb részét lefedik. A sokdimenziós pontfelhőt erre a három tengelyre vetíti le, így kapunk egy forgatható 3D térképet.

**4. A diákok beillesztése (ízlésvektorok)**

A térképen a diákok a középpontból kiinduló nyilakként jelennek meg. A nyíl iránya azt mutatja, hogy az adott ember a 3D tér melyik sarka felé húz, vagyis merre találhatók azok a dalok, amiket a saját átlagához képest a leginkább szeretett. Ha két diák nyila közel párhuzamos, az ízlésük rokon; ha egymással szembe mutatnak, akkor a csoport két ellenpólusát képviselik. 

...

## Mi a matek?

Az értékeléseket először diákonként centráljuk és skálázzuk $z$-értékekké ($z_{ij} = \frac{x_{ij} - \mu_j}{\sigma_j}$), ami semlegesíti az egyéni értékelői torzításokat (például az általános megengedőséget vagy szigort). Matematikailag két standardizált vektor, $\mathbf{z}_a$ és $\mathbf{z}_b$ négyzetes euklideszi távolsága $n$ dal esetén a következő összefüggést követi:

$$\Vert{}\mathbf{z}_a - \mathbf{z}_b\Vert{}^2 = \sum_{i=1}^{n} (z_{ia} - z_{ib})^2 = 2(n - 1)(1 - r_{ab})$$

ahol $r_{ab}$ a Pearson-féle korrelációs együttható. Mivel ez a kapcsolat szigorúan monoton, a standardizált koordinátákon számított euklideszi távolság matematikailag egyenértékű a Pearson-féle korrelációs távolság $(1 - r)$ alapján történő klaszterezéssel. A pontok nem az abszolút numerikus pontszámok azonossága miatt csoportosulnak, hanem azért, mert a relatív értékelési csúcsaik és mélypontjaik következetesen együtt mozognak (kovariálnak) a mintában.

A standardizált, $n \times p$ dimenziós $\mathbf{Z}$ mátrixot (dalok $\times$ diákok) ezután szinguláris érték felbontással (SVD) dekomponáljuk: $\mathbf{Z} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T$. A főkomponens-elemzés (PCA) meghatározza a mintakovariancia-mátrix azon három ortogonális sajátvektorát, amelyek a lehető legtöbb közös értékelési varianciát fedik le. A dalok 3D koordinátáit a főkomponens-pontszámok mátrixa adja meg ($\mathbf{T}_3 = \mathbf{Z}\mathbf{V}_3$), míg a diákok a $\mathbf{V}_3$ segítségével meghatározott súlyvektorokként (loadings) vetülnek a térbe. Mivel ez az alacsony rangú faktorizáció a standardizált értékeket a $\mathbf{Z} \approx \mathbf{T}_3 \mathbf{V}_3^T$ formulával rekonstruálja, egy adott dal térbeli pozíciójának ($\mathbf{t}_i$) és egy diák súlyvektorának ($\mathbf{v}_j$) skaláris szorzata éppen a diák becsült standardizált preferenciáját ($\hat{z}_{ij}$) adja. Következésképpen az azonos szavazási mintázatot kapott dalok a térben egymás mellé rendeződnek, a diákok vektorai pedig közvetlenül azon dalcsoportok felé mutatnak, amelyeket a saját átlagukhoz képest a legmagasabbra értékeltek.

```

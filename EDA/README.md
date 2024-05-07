# Hotele na wakacje

## Cel

Celem niniejszego projektu jest stworzenie systemu **klasyfikacji** hoteli na podstawie dostępnych danych. Pragniemy opracować model, który będzie w stanie przewidzieć **ocenę (rating) hotelu** na podstawie różnorodnych cech, takich jak lokalizacja, kategoria ceny, udogodnienia i innych. Dążymy do stworzenia modelu, który zapewni użytkownikom możliwie najdokładniejsze rekomendacje dotyczące jakości i atrakcyjności hoteli, co przyczyni się do usprawnienia procesu podejmowania decyzji przez potencjalnych gości.


## Dane

1.  Dane pochodzą z **Tripadvisor API**. Wysyłamy zapytania do API w następującym formacie:
 ```
 https://api.content.tripadvisor.com/api/v1/location/{locationId}/details
```
2.  Dla pobierania locationId hoteli, w korzystamy z **scrappera** i strony wyszukiwań Tripadvisor, gdzie locationId jest wybrany ręcznie id miasta lub kraju. offset odstęp od początku wyszukiwań, potrzebujemy go, bo strona wyszukiwań pokazuję tylko 30 hoteli:

```
https://www.tripadvisor.com/Hotels-g{locationId}-{offset}
```
3. Żądanie do API dotyczące szczegółów lokalizacji zwraca kompleksowe informacje na temat lokalizacji hotelu, nazwa, adres, ocena, adresy URL wpisu na stronie Tripadvisor i inne informacje w formacie **JSON**.
4.  Przeanalizujemy i przekonwertujemy JSONy z informacją o hotelach do **CSV** pliku w wyniku mamy taką strukturę dla 1166 hoteli:
* **id** (int) Identyfikator hotelu w razie potrzeby uzyskania dodatkowych informacji z Tripadvisor
* **name** (str) Nazwa hotelu w razie potrzeby uzyskania dodatkowych informacji spoza Tripadvisor
* **region** (str) Region
* **country** (str) Kraj
* **latitude** (float) Szerokość geograficzna tej lokalizacji w stopniach
* **longitude** (float) Długość geograficzna tej lokalizacji w stopniach
* **ranking** (int) Miejsce w rankingu w tym samym miejscu docelowym
* **ranking_out_of** (int) Liczba hoteli w rankingu w tym samym miejscu docelowym
* **rating** (float) Ocena hotelu
* **num_reviews** (int) Liczba wszystkich recenzji opublikowanych dla hotelu
* **photo_count** (int) Liczba zdjęć hotelu opublikowanych na stronie Tripadvisor
* **amenities** (str) Udogodnienia oferowane przez ten hotel
* **brand** (str) marka tego hotelu
* **awards** (str) Nagrody hotelu
* **price_level** (str) Względny poziom ceny dla hotelu

## Wstępna ocena i przygotowanie

### Rating

Przekształcimy ocenę do dwóch kategorii
![image](https://hackmd.io/_uploads/Hy1sPLrqa.png)
![image](https://hackmd.io/_uploads/HyYeiLSqp.png)
W modelowaniu będziemy używać 1 dla `Very good` i 0 dla `Good`

### Country

Za pomocą przedstawionej wizualizacji zauważalna jest korelacja pomiędzy ocenami hoteli a poszczególnymi krajami.
![image](https://hackmd.io/_uploads/rkjb4DScT.png)

### Region

Również zauważalna jest korelacja pomiędzy ocenami hoteli a poszczególnymi regionami. Regiony zawierają taką samą informację, że kraje więc zbędne będzie zostawienie dwóch cech.
![image](https://hackmd.io/_uploads/SJ-J8PHc6.png)

### City

Podział na miasta był za mały, więc nie dodałem do modelu.

![image](https://hackmd.io/_uploads/BJhZPwB5a.png)


### Price level

Ceny mamy podane w formacie `$$$$, $$$, $$, $`. 
Przekształcimy na liczby `df.price_level.apply(len)`

![image](https://hackmd.io/_uploads/S1uZrurcp.png)

### Ranking and Ranking out of

Rozważymy możliwość połączenia dwóch w jedną zmienną.
```python
df['ranking_relation'] = round(df.ranking / df.ranking_out_of, 2)
df['binned_ranking_relation'] = pd.cut(df['ranking_relation'], bins=5)
```

![image](https://hackmd.io/_uploads/SkZHO_B56.png)

### Amenities

Kodujemy udogodnienia za pomocą dummy variables. Z wizualizacji widzimy, że to nam przyda.
![image](https://hackmd.io/_uploads/BJ2o3OH56.png)

Ale mamy w takim razie 288 nowych kolumn, które dają podobny wynik oceny.
![image](https://hackmd.io/_uploads/HytpPwD9a.png)

Zdecydowałem zakodować udogodnienia w liczbę udogodnień każdego hotelu. Jak widzimy, że średnia ocena rośnie z większą liczba udogodnień.

![image](https://hackmd.io/_uploads/rJW5wvD56.png)


### Awards

Też używając dummy, kodujemy nagrody, widzimy różnice dla hoteli z nagrodami i bez.
![image](https://hackmd.io/_uploads/ry00nfU56.png)

Możemy zauważyć, że większość hoteli z nagrodami należy do oceny jeden więc my możemy po prostu zostawić 1 jeżeli chociażby jedna nagroda jest i 0 w innym przypadku.

![image](https://hackmd.io/_uploads/HyMJucU9a.png)

### Brand

Większość hoteli nie ma przypisanej marki, więc możemy zakodować zero-jedynkowo i widzimy, że nam to też przyda.

![image](https://hackmd.io/_uploads/rJQwNdP9p.png)

### Podsumowanie

Wynik połączenia cech w heatmap.

![image](https://hackmd.io/_uploads/HJbfVEdca.png)


## Modelowanie i ewaluacja

### KNN

```python
KNeighborsClassifier(n_neighbors=9)
```
Dokładność po walidacji krzyżowej **0.82**

Macierz pomyłek dla wybranego zbioru walidacyjnego.
|     | Precision | Recall | f1-score |
| --- |:---------:| ------:| --------:|
| 0   |   0.77    |   0.76 |     0.76 |
| 1   |   0.84    |   0.85 |     0.85 |


![image](https://hackmd.io/_uploads/BJpa-TO9T.png)

### Random forest classifier

```python
RandomForestClassifier(n_estimators=600, max_depth=8, max_features='sqrt', criterion='entropy')
```
Dokładność po walidacji krzyżowej **0.85**

Macierz pomyłek dla wybranego zbioru walidacyjnego.
|     | Precision | Recall | f1-score |
| --- |:---------:| ------:| --------:|
| 0   |   0.81    |   0.65 |     0.72 |
| 1   |   0.80    |   0.90 |     0.85 |


![image](https://hackmd.io/_uploads/rJxvhNKcT.png)


### Logistic regression

```python
LogisticRegression()
```
Dokładność po walidacji krzyżowej **0.82**

Macierz pomyłek dla wybranego zbioru walidacyjnego.
|     | Precision | Recall | f1-score |
| --- |:---------:| ------:| --------:|
| 0   |   0.81    |   0.59 |     0.69 |
| 1   |   0.77    |   0.91 |     0.84 |

![image](https://hackmd.io/_uploads/HJcIL8t5p.png)


### Linear Discriminant Analysis

```python
LDA(store_covariance=True)
```
Dokładność po walidacji krzyżowej **0.83**

Macierz pomyłek dla wybranego zbioru walidacyjnego.
|     | Precision | Recall | f1-score |
| --- |:---------:| ------:| --------:|
| 0   |   0.79    |   0.59 |     0.68 |
| 1   |   0.77    |   0.89 |     0.83 |

![image](https://hackmd.io/_uploads/HkewtIY5p.png)

## Wynik i wnioski

Po ewaluacji i selekcji modeli ja wybrałem **KNN**. Daje podobną dokładność do RFC, ale jest prosty w implementacji i nie mamy dużego zbioru danych więc koszt obliczeniowy nie jest wysoki.

Dokładność zbioru testowego **0.81**

Macierz pomyłek dla wybranego zbioru testowego.
|     | Precision | Recall | f1-score |
| --- |:---------:| ------:| --------:|
| 0   |   0.71    |   0.68 |     0.69 |
| 1   |   0.85    |   0.87 |     0.86 |

![image](https://hackmd.io/_uploads/Bkp728Fc6.png)





















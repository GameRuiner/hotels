# 🏨 HotelMatcher – System Rekomendacji Hoteli

**HotelMatcher** to projekt mający na celu stworzenie systemu rekomendacji hoteli na podstawie danych zebranych z serwisu TripAdvisor. Projekt składa się z dwóch głównych komponentów:

- **WebScraper** Moduł odpowiedzialny za zbieranie danych o hotelach i recenzjach z TripAdvisor.
- **EDA** Moduł eksploracyjnej analizy danych oraz budowy modeli predykcyjnych.

## 🧾 Opis projektu

### 🎯 Cel

Celem projektu jest zbieranie danych o hotelach, takich jak lokalizacja, kategoria ceny, udogodnienia i innych. Drugi etap to stworzenia modelu, który zapewni użytkownikom możliwie najdokładniejsze rekomendacje dotyczące jakości i atrakcyjności hoteli, co przyczyni się do usprawnienia procesu podejmowania decyzji przez potencjalnych gości.

### 🗂️ Struktura projektu

```
hotels/
├── EDA/                 # Eksploracyjna analiza danych i modele predykcyjne
│   ├── data_preparation.ipynb
│   ├── hotels_visualization.ipynb
│   ├── price_modeling.ipynb
│   ├── rating_modeling.ipynb
│   ├── hotels.csv
│   ├── hotels2.csv
│   └── ...
├── WebScraper/          # Skrypty do pobierania danych z TripAdvisor
│   ├── fetch_hotels.py
│   ├── fetch_reviews.py
│   ├── parse_hotel_pages.py
│   ├── fetched_cities.json
│   └── ...
├── EDA_mongo.ipynb      # Analiza danych z MongoDB
├── recomendation.ipynb  # Notebook z systemem rekomendacji
├── preembedding.py      # Skrypt przygotowujący dane do embeddingu
└── ...
```

## 🛠️ Technologie

- **Języki programowana**: Python
- **Biblioteki i narzędzia**
  - Scrapowanie danych: `requests`, `BeautifulSoup`, `Selenium`
  - Analiza danych: `pandas`, `numpy`, `matplotlib`, `seaborn`
  - Uczenie maszynowe: `scikit-learn`
  - Baza danych: `MongoDB`

## 🔧 Instalaca

1. Sklonuj repozyorium:

```bash
git clone https://github.com/GameRuiner/hotels.git
```

2. Zainstaluj wymagane bibloteki:

```bash
pip install -r requirements.txt
```

3. Skonfiguruj plik `.env` na podstawie `.env.example`, uzupełniając dane dostępowe do MongoDB.

4. Uruchom skrypty do zbierania danych znajdujące się w katalogu `WebScraper`.

5. Przeprowadź analizę danych i budowę modeli, korzystając z notebooków w katalogu`EDA`.

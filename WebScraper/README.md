# Web scraper z MongoDB

Projekt polega na wykorzystaniu języka Python do scrapowania danych z strony oraz API TripAdvisor w celu pozyskania informacji o hotelach i recenzjach. Następnie zebrane dane są zapisywane w bazie danych MongoDB. Dane te mogą być później wykorzystane do uczenia maszynowego oraz analizy.


## Składniki:

1. **Scrapowanie danych**:
   * Skrypty napisane w języku Python są wykorzystywane do scrapowania danych ze strony oraz API TripAdvisor.
   * Zbierane informacje o hotelach i odpowiadających im recenzjach
2. **Przechowywanie danych**:
   * Do przechowywania zebranych danych używana jest baza danych MongoDB.
   * Dane sązapisane w kolekcjach w bazie danych MongoDB w celu łatwego pobierania i zarządzania nimi.
3. **Wykorzystanie danych**:
   * Zebrane zbiory danych stanowią cenne zasoby do zastosowań w uczeniu maszynowym.
   * Ponadto dane są analizowane, aby wyciągać wnioski i trendy w branży hotelarskiej.

## Instrukcje konfiguracji:

1. **Konfiguracja środowiska:**
   * Upewnij się, że na Twoim systemie zainstalowany jest język Python.
   * Zainstaluj niezbędne pakiety języka Python za pomocą pip lub conda.
   * Klucz od TripAdvisor API zapisz do pliku `.env` do zmiennej `TRIPADVISOR_KEY`.
2. **Instalacja MongoDB:**
   * Zainstaluj MongoDB i skonfiguruj lokalną instancję lub połącz się z zdalnym serwerem MongoDB.
   * Ścieżkę połączenie do bazy danych zapisz do pliku `.env` do zmiennej `MONGO_HOST`.
3. **Skrypty w języku Python**:
   * `crawler.py` służy do scrapowania identyfikatorów hoteli.
   * `fetch_hotels.py` pobiera dane hoteli za pomocą API TripAdvisor, których identyfikatory są zapisane w `ids.txt`.
   * `fetch_reviews.py` dla hoteli, które nie mają opinij w bazie danych pobiera za pomocą API TripAdvisor opinie.

## Użycie:

1. **Dostęp do danych:**
   * Pobierz przechowywane dane z bazy danych MongoDB w celu dalszej analizy lub zadań związanych z uczeniem maszynowym.
   * Wykorzystaj zapytania MongoDB, aby wydobyć cenne wnioski i trendy w dziedzinie hotelarstwa.


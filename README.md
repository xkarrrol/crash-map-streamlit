# Przestrzenna Analiza Wypadków w NYC 

Interaktywna aplikacja webowa do analizy przestrzennej kolizji drogowych w Nowym Jorku. Projekt wizualizuje hotspoty wypadków i trendy czasowe, wykorzystując zoptymalizowany format danych Parquet oraz trójwymiarową agregację heksagonalną.

**Wersja Live:** 
https://crash-map-app.streamlit.app/

## Kluczowe funkcje
* **Agregacja przestrzenna:** Wykorzystanie `HexagonLayer` z biblioteki PyDeck do renderowania map gęstości w 3D. Zapobiega to przeciążeniu przeglądarki przy rysowaniu dziesiątek tysięcy punktów.
* **Analiza czasowa:** Dynamiczne wykresy wygenerowane w Plotly, reagujące w czasie rzeczywistym na filtry (pora dnia, dzielnica, typ obrażeń).
* **Optymalizacja danych (ETL):** Surowy zbiór danych z NYC Open Data został oczyszczony z wierszy pozbawionych współrzędnych i poddany konwersji do skompresowanego formatu `.parquet`. 

## Stack technologiczny
* Python, Streamlit, Pandas, PyDeck, Plotly, PyArrow

## Uruchomienie lokalne
```bash
pip install -r requirements.txt
streamlit run app.py

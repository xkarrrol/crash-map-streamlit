# Przestrzenna Analiza Wypadków w NYC 

Interaktywna aplikacja webowa do analizy przestrzennej kolizji drogowych w Nowym Jorku. Projekt wizualizuje hotspoty wypadków i trendy czasowe, wykorzystując zoptymalizowany format danych Parquet oraz trójwymiarową agregację heksagonalną.

---

**Wersja Live:** 
[![Streamlit App](https://streamlit.io)](https://crash-map-app.streamlit.app/)

---

<img width="1793" height="826" alt="map" src="https://github.com/user-attachments/assets/17b97e08-5b8a-45ec-afcf-54422f0f39f9" />

---

<img width="1822" height="782" alt="wykres" src="https://github.com/user-attachments/assets/9f89e55d-db07-4266-9e47-dcb0a5cc3349" />

---

## Kluczowe funkcje
* **Agregacja przestrzenna:** Wykorzystanie `HexagonLayer` z biblioteki PyDeck do renderowania map gęstości w 3D. Zapobiega to przeciążeniu przeglądarki przy rysowaniu dziesiątek tysięcy punktów.
* **Analiza czasowa:** Dynamiczne wykresy wygenerowane w Plotly, reagujące w czasie rzeczywistym na filtry (pora dnia, dzielnica, typ obrażeń).
* **Optymalizacja danych (ETL):** Surowy zbiór danych z NYC Open Data został oczyszczony z wierszy pozbawionych współrzędnych i poddany konwersji do skompresowanego formatu `.parquet`.

---

## Stack technologiczny
* Python, Streamlit, Pandas, PyDeck, Plotly, PyArrow

---

### Źródło danych
* **Zbiór:** [Motor Vehicle Collisions – Crashes (NYC Open Data)](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/about_data)
* **Wydawca:** NYPD / NYC Open Data
* **Opis:** Oficjalne dane o kolizjach i wypadkach drogowych w Nowym Jorku.

---

## Uruchomienie lokalne
```bash
pip install -r requirements.txt
streamlit run app.py

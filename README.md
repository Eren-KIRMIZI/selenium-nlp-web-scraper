## Smart Web Scraper

Modern web scraping pipeline with NLP analysis and interactive dashboards.

Bu proje, web sitelerinden otomatik veri toplayan, toplanan metinleri yapay zeka ile analiz eden ve sonuçları dashboard'larda sunan uçtan uca bir sistemdir.

Selenium ile web siteleri taranır, spaCy ile metinlerden anlamlı bilgiler (isimler, yerler vb.) çıkarılır, veri temizlenir ve Flask + Streamlit ile görselleştirilir.

**Kısaca:**  
scraping + NLP + görselleştirme = tek tuşla veri analizi 

---

## Screenshots

<img width="1339" src="https://github.com/user-attachments/assets/903ee924-e42d-46dd-9217-b193f751402e" />
<img width="1339" src="https://github.com/user-attachments/assets/8d0e6490-73f7-4493-ae05-ba8d08fee6c4" />
<img width="1315" src="https://github.com/user-attachments/assets/e64f0c01-3fa9-4875-935f-6de1c621ad31" />

---

## Features

- **Web Scraping**: Selenium-based dynamic content scraping  
- **NLP Analysis**: spaCy integration for entity detection and POS tagging  
- **Data Quality**: Automated cleaning and validation  
- **Dual Dashboards**:
  - Flask (Web Dashboard)
  - Streamlit (Analytics Panel)
- **REST API**: JSON endpoints for data access  

---

## Tech Stack

- Python 3.x  
- Selenium WebDriver  
- spaCy NLP  
- Flask  
- Streamlit  
- Pandas  

---

## Run Full Pipeline

Tüm scraping + NLP + veri kalite sürecini çalıştırmak için:

```bash
python scheduler.py
```

## Flask Dashboard:
```bash
python app.py
```
Visit http://127.0.0.1:5000

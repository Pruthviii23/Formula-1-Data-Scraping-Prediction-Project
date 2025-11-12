# 🏁 Formula 1 Data Scraping & Prediction Project

### 📘 Overview
This project is a part of my **college data analytics assignment**, focused on **scraping, integrating, and analyzing Formula 1 racing data** from multiple seasons (2016–2024).  
The main goal is to build a **comprehensive dataset** that can later be used for **machine learning tasks**, such as predicting top finishers in future races.

---

## ⚙️ Project Structure

```
📂 f1/
│
├── f1_scraper.py                              # Scraping data from https://www.formula1.com
│
├── f1_datasets/                               # Collection of the datasets
│   ├── f1_fastest_laps.csv
│   ├── f1_pit_stop_summary.csv
│   ├── f1_race_results.csv 
│   ├── f1_practice1_results.csv
│   ├── f1_qualifying_results.csv
│   └── f1_master_dataset_2016_2024.csv
│
├── integrate.py                               # Data integration and enrichment pipeline
├── race_urls_2016_2024.txt                    # URLs for all races (2016–2024)
└── README.md
```

---

## 🌐 Data Sources

All data was **scraped from publicly available Formula 1 results pages** on the official F1 website:  
🔗 [https://www.formula1.com/en/results.html](https://www.formula1.com/en/results.html)

Data collected includes:
- Race Results  
- Qualifying Results  
- Fastest Laps  
- Pit Stop Summary  
- Practice 1 Session Times  

Each dataset spans **nine Formula 1 seasons (2016–2024)**.

---

## 🧰 Tools & Libraries

| Category | Tools Used |
|-----------|-------------|
| **Scraping** | Selenium, BeautifulSoup, webdriver-manager |
| **Data Processing** | Pandas, NumPy |
| **Environment** | Python 3.11 |

---

## 🧩 Data Integration

The individual datasets (race, qualifying, practice, etc.) were merged using common keys:  
`Season`, `Race`, and `Driver`.  

The integrated dataset includes metrics like:
- Practice 1 time (pre-race pace indicator)  
- Qualifying position (starting grid)  
- Pit stop count (race strategy proxy)  
- Fastest lap time  
- Points, Laps, Finishing position  

This creates a **rich, multi-dimensional dataset** suitable for predictive modeling.

---

## ⚔️ Challenges Faced

1. **Dynamic Web Pages (JS Rendering)** —  
   The Formula1.com website loads content asynchronously, making static scraping fail.  
   ✅ Solution: Used Selenium WebDriver with intelligent waits and dynamic scrolling.

2. **Data Inconsistency Across Years** —  
   Table structures slightly changed between seasons.  
   ✅ Solution: Used flexible XPath selectors and fallback logic.

3. **Session Data Missing for Some Races** —  
   Practice or pit-stop pages sometimes unavailable.  
   ✅ Solution: Handled gracefully by skipping with warnings and merging only available data.

---

## 🧩 Future Goals

🚀 **Data Expansion**
- Integrate weather, track temperature, and circuit type via Meteostat and Wikipedia.

## 🧠 Machine Learning Objective

The first predictive goal was to estimate **the probability of a driver finishing in the Top 5** in a race.  
Models explored:
- ✅ XGBoost Classifier (primary model)
- 🚧 Planned: LightGBM, Neural Networks, and Ranking Models

### Input Features
Pre-race features such as:
- Qualifying position  
- Practice session times  
- Previous performance averages  

### Target
Binary classification:  
`Top5 = 1` if driver finished ≤5th, else `0`.

🧠 **Advanced Modeling**
- Add ranking/regression models to predict exact finishing positions.
- Experiment with deep learning architectures (LSTM/MLP).

📊 **Analytics Dashboard**
- Build an interactive F1 analytics dashboard using Streamlit or Plotly Dash to visualize:
  - Team consistency
  - Driver improvement curves
  - Pre-race performance predictors

---

## 📚 Academic Context

This project was created as part of a **Data Analytics & Machine Learning coursework assignment**.  
The intention was to:
- Demonstrate end-to-end data handling (collection → cleaning → modeling)  
- Showcase real-world application of ML on a sports dataset  
- Build a reusable dataset for future research and analysis  

---

## 🤝 Contribution & Usage

Feel free to:
- Fork this repository  
- Use the scraping scripts to update future race data  
- Extend the dataset for your own F1 analytics or AI projects  

---

## 🏎️ Final Note

This project was designed with both **educational value** and **real-world utility** in mind.  
It’s meant to serve as a foundation for **data-driven motorsport analysis** —  
from performance insights to predictive AI applications in Formula 1.

> *"Data is the fuel, speed is the outcome."* 💡

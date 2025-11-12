from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time, os, re

# ================== CONFIG ==================
TXT_FILE = "race_urls_2016_2024.txt"
HEADLESS = True
WAIT_TIMEOUT = 15
SCROLL_PAUSE = 1.0

# ================== SELENIUM SETUP ==================
options = Options()
if HEADLESS:
    options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def wait_for_table():
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )

# ================== GENERIC TABLE SCRAPER ==================
def scrape_table(url, year, race_name, column_map):
    print(f"📄 Scraping: {url}")
    driver.get(url)
    try:
        wait_for_table()
    except:
        print(f"⚠️ No table found at {url}")
        return []

    time.sleep(SCROLL_PAUSE)
    rows = driver.find_elements(By.XPATH, "//tr[contains(@class,'Table-module_body-row')]")
    data = []

    for r in rows:
        cols = r.find_elements(By.TAG_NAME, "td")
        if len(cols) < len(column_map):
            continue

        entry = {"Season": year, "Race": race_name, "SourceURL": url}
        for key, idx in column_map.items():
            try:
                entry[key] = cols[idx].text.strip()
            except:
                entry[key] = ""
        data.append(entry)

    print(f"✅ {len(data)} rows collected from {url}")
    return data

# ================== SCRAPER FUNCTIONS ==================
def scrape_race_results(url, year, race):
    return scrape_table(url, year, race, {
        "Position": 0,
        "Driver": 2,
        "Team": 3,
        "Laps": 4,
        "Time/Retired": 5,
        "Points": 6
    })

def scrape_qualifying(url, year, race):
    return scrape_table(url, year, race, {
        "Position": 0,
        "Driver": 2,
        "Team": 3,
        "Q1": 4,
        "Q2": 5,
        "Q3": 6
    })

def scrape_fastest_laps(url, year, race):
    return scrape_table(url, year, race, {
        "Position": 0,
        "Driver": 2,
        "Team": 3,
        "Lap": 4,
        "Time": 5,
        "Speed (km/h)": 6
    })

def scrape_practice1(url, year, race):
    return scrape_table(url, year, race, {
        "Position": 0,
        "Driver": 2,
        "Team": 3,
        "Time": 4,
        "Laps": 5
    })

def scrape_pit_stop_summary(url, year, race):
    return scrape_table(url, year, race, {
        "Stop": 0,
        "Driver": 1,
        "Team": 2,
        "Lap": 3,
        "Time of Day": 4,
        "Time": 5,
        "Total": 6
    })


# ================== PARSE URL FILE ==================
def parse_race_urls(file_path):
    races = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    current_year, current_race = None, None
    current_urls = {}

    for line in lines:
        if line.startswith("###"):
            match = re.match(r"###\s*(\d{4})\s*-\s*(.+?)\s*###", line)
            if match:
                if current_year and current_urls:
                    races.append((current_year, current_race, current_urls))
                current_year = match.group(1)
                current_race = match.group(2)
                current_urls = {}
        else:
            if "race-result" in line:
                current_urls["race"] = line
            elif "qualifying" in line:
                current_urls["qualifying"] = line
            elif "fastest-laps" in line:
                current_urls["fastest"] = line
            elif "practice/1" in line:
                current_urls["practice1"] = line
            elif "pit-stop-summary" in line:
                current_urls["pitstop"] = line

    if current_year and current_urls:
        races.append((current_year, current_race, current_urls))

    return races


# ================== MAIN LOOP ==================
os.makedirs("f1_datasets", exist_ok=True)

races = parse_race_urls(TXT_FILE)
races_all, qualy_all, fast_all, fp1_all, pits_all = [], [], [], [], []

for year, race, urls in races:
    print(f"\n🏁 {year} - {race}")
    if "race" in urls:
        races_all.extend(scrape_race_results(urls["race"], year, race))
    if "qualifying" in urls:
        qualy_all.extend(scrape_qualifying(urls["qualifying"], year, race))
    if "fastest" in urls:
        fast_all.extend(scrape_fastest_laps(urls["fastest"], year, race))
    if "practice1" in urls:
        fp1_all.extend(scrape_practice1(urls["practice1"], year, race))
    if "pitstop" in urls:
        pits_all.extend(scrape_pit_stop_summary(urls["pitstop"], year, race))

# ================== SAVE TO CSV ==================
pd.DataFrame(races_all).to_csv("f1_datasets/f1_race_results.csv", index=False)
pd.DataFrame(qualy_all).to_csv("f1_datasets/f1_qualifying_results.csv", index=False)
pd.DataFrame(fast_all).to_csv("f1_datasets/f1_fastest_laps.csv", index=False)
pd.DataFrame(fp1_all).to_csv("f1_datasets/f1_practice1_results.csv", index=False)
pd.DataFrame(pits_all).to_csv("f1_datasets/f1_pit_stop_summary.csv", index=False)

print("\n✅ All data successfully saved under /f1_datasets/")
driver.quit()
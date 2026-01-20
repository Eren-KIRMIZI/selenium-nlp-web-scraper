from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime

def scrape_quotes():
    """
    Quotes to Scrape sitesinden alıntıları çeker
    """
    print("Scraping başlatılıyor...")
    
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Görmek istersen bunu yorum yap
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://quotes.toscrape.com/js/")
        
        # JavaScript'in yüklenmesini bekle
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "quote")))
        time.sleep(2)
        
        items = []
        quotes = driver.find_elements(By.CLASS_NAME, "quote")
        
        print(f"{len(quotes)} adet alıntı bulundu")
        
        for quote in quotes:
            try:
                text = quote.find_element(By.CLASS_NAME, "text").text
                author = quote.find_element(By.CLASS_NAME, "author").text
                tags = quote.find_elements(By.CLASS_NAME, "tag")
                tag_list = [tag.text for tag in tags]
                
                items.append({
                    "text": text,
                    "author": author,
                    "tags": ", ".join(tag_list),
                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            except Exception as e:
                print(f"Bir quote işlenirken hata: {e}")
                continue
        
        driver.quit()
        
        df = pd.DataFrame(items)
        df.to_csv("data.csv", index=False, encoding='utf-8')
        
        print(f"{len(items)} alıntı data.csv'ye kaydedildi")
        return df
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
        driver.quit()
        return None

if __name__ == "__main__":
    scrape_quotes()
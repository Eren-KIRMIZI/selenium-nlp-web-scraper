from scraper import scrape_quotes
from nlp_analysis import nlp_process
from analysis import analyze
from datetime import datetime
import sys

def run_pipeline():
    """
    Tüm pipeline'ı sırayla çalıştırır
    """
    print("=" * 60)
    print("SMART SCRAPER PIPELINE BAŞLATILIYOR")
    print(f"Zaman: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # 1. SCRAPING
        print("\nADIM 1/3: Web Scraping")
        print("-" * 60)
        df = scrape_quotes()
        if df is None or df.empty:
            print("Scraping başarısız!")
            return False
        
        # 2. NLP ANALYSIS
        print("\nADIM 2/3: NLP Analysis")
        print("-" * 60)
        df = nlp_process()
        if df is None:
            print("NLP analizi başarısız!")
            return False
        
        # 3. DATA QUALITY ANALYSIS
        print("\nADIM 3/3: Data Quality Analysis")
        print("-" * 60)
        report = analyze()
        if report is None:
            print("Analiz başarısız!")
            return False
        
        # BAŞARI
        print("\n" + "=" * 60)
        print("PIPELINE BAŞARIYLA TAMAMLANDI!")
        print("=" * 60)
        print("\nOluşturulan dosyalar:")
        print("  • data.csv     → Temiz veri")
        print("  • report.json  → Kalite raporu")
        print("\nDashboard'u başlat:")
        print("  • Flask: python app.py")
        print("  • Streamlit: streamlit run dashboard_advanced.py")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\nPIPELINE HATASI: {e}")
        return False

if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)
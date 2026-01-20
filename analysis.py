import pandas as pd
import json
from datetime import datetime

def analyze():
    """
    Veri kalitesi analizi yapar ve rapor oluşturur
    """
    print("Veri kalite analizi başlatılıyor...")
    
    try:
        df = pd.read_csv("data.csv")
    except FileNotFoundError:
        print("data.csv bulunamadı!")
        return None
    
    initial_rows = len(df)
    
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "initial_stats": {
            "total_rows": initial_rows,
            "columns": list(df.columns),
        },
        "data_quality": {
            "missing_text": int(df["text"].isnull().sum()),
            "missing_author": int(df["author"].isnull().sum()),
            "duplicates": int(df.duplicated(subset=["text"]).sum()),
        },
        "text_analysis": {
            "avg_text_length": float(df["text_length"].mean()) if "text_length" in df.columns else 0,
            "avg_word_count": float(df["word_count"].mean()) if "word_count" in df.columns else 0,
        },
        "authors": {
            "unique_authors": int(df["author"].nunique()),
            "top_authors": df["author"].value_counts().head(5).to_dict()
        }
    }
    
    # Veri temizleme
    df.drop_duplicates(subset=["text"], inplace=True)
    df = df[df["text"].str.strip() != ""]
    df.dropna(subset=["text", "author"], inplace=True)
    
    final_rows = len(df)
    report["cleaning_results"] = {
        "rows_before": initial_rows,
        "rows_after": final_rows,
        "rows_removed": initial_rows - final_rows,
    }
    
    df.to_csv("data.csv", index=False, encoding='utf-8')
    
    with open("report.json", "w", encoding='utf-8') as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    
    print(f"Analiz tamamlandı! {initial_rows} → {final_rows} satır")
    return report

if __name__ == "__main__":
    analyze()
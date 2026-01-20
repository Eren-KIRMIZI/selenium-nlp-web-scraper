from flask import Flask, render_template, jsonify
import pandas as pd
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    """
    Ana dashboard sayfası
    """
    return render_template("index.html")

@app.route("/api/stats")
def api_stats():
    """
    Dashboard için tüm istatistikleri döndür
    """
    try:
        df = pd.read_csv("data.csv")
        with open("report.json", "r", encoding='utf-8') as f:
            report = json.load(f)
        
        # Top authors
        top_authors_data = df["author"].value_counts().head(5)
        max_count = top_authors_data.max() if len(top_authors_data) > 0 else 1
        
        top_authors = []
        for author, count in top_authors_data.items():
            top_authors.append({
                "author": author,
                "count": int(count),
                "percentage": round((count / max_count * 100), 2)
            })
        
        # NaN değerlerini temizle
        df_clean = df.fillna({
            'word_count': 0,
            'text_length': 0,
            'entities': 'None',
            'pos_tags': 'None',
            'tags': ''
        })
        
        # Son 10 quote'u al ve NaN'leri temizle
        recent_quotes = df_clean.head(10).to_dict('records')
        
        # Her bir quote'taki NaN'leri kontrol et
        for quote in recent_quotes:
            for key, value in quote.items():
                if pd.isna(value):
                    quote[key] = None if isinstance(value, str) else 0
        
        return jsonify({
            "total_quotes": len(df),
            "unique_authors": int(df["author"].nunique()),
            "avg_word_count": round(df["word_count"].mean(), 1) if "word_count" in df.columns and not df["word_count"].isna().all() else 0,
            "avg_text_length": round(df["text_length"].mean(), 1) if "text_length" in df.columns and not df["text_length"].isna().all() else 0,
            "top_authors": top_authors,
            "recent_quotes": recent_quotes,
            "timestamp": report["timestamp"],
            "rows_after": report["cleaning_results"]["rows_after"],
            "rows_removed": report["cleaning_results"]["rows_removed"],
            "missing_text": report["data_quality"]["missing_text"],
            "duplicates": report["data_quality"]["duplicates"]
        })
        
    except FileNotFoundError as e:
        return jsonify({"error": f"Veri bulunamadı: {str(e)}"}), 404
    except Exception as e:
        return jsonify({"error": f"Sunucu hatası: {str(e)}"}), 500

@app.route("/api/data")
def api_data():
    """
    JSON API endpoint
    """
    try:
        df = pd.read_csv("data.csv")
        # NaN değerlerini temizle
        df = df.fillna({
            'word_count': 0,
            'text_length': 0,
            'entities': 'None',
            'pos_tags': 'None',
            'tags': ''
        })
        return jsonify(df.to_dict('records'))
    except FileNotFoundError:
        return jsonify({"error": "data.csv bulunamadı"}), 404

@app.route("/api/report")
def api_report():
    """
    Rapor API endpoint
    """
    try:
        with open("report.json", "r", encoding='utf-8') as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({"error": "report.json bulunamadı"}), 404

if __name__ == "__main__":
    print("Flask Dashboard başlatılıyor...")
    print("http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
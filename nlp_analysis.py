import spacy
import pandas as pd
from collections import Counter

try:
    nlp = spacy.load("en_core_web_sm")
except:
    print("spaCy modeli bulunamadı!")
    print("Lütfen şunu çalıştır: python -m spacy download en_core_web_sm")
    exit()

def nlp_process():
    """
    CSV'deki metinleri NLP ile analiz eder
    """
    print("NLP analizi başlatılıyor...")
    
    try:
        df = pd.read_csv("data.csv")
    except FileNotFoundError:
        print("data.csv bulunamadı! Önce scraper.py çalıştır.")
        return None
    
    if df.empty:
        print("CSV boş!")
        return None
    
    entities = []
    pos_tags = []
    word_counts = []
    
    print(f"{len(df)} metin analiz ediliyor...")
    
    for idx, text in enumerate(df["text"].fillna(""), 1):
        doc = nlp(text)
        
        # Entity detection
        ents = [f"{ent.text} ({ent.label_})" for ent in doc.ents]
        entities.append(", ".join(ents) if ents else "None")
        
        # POS tagging
        pos_count = Counter([token.pos_ for token in doc])
        pos_tags.append(f"NOUN:{pos_count.get('NOUN', 0)} VERB:{pos_count.get('VERB', 0)}")
        
        # Word count
        word_counts.append(len([token for token in doc if not token.is_punct]))
        
        if idx % 5 == 0:
            print(f"{idx} metin işlendi")
    
    df["entities"] = entities
    df["pos_tags"] = pos_tags
    df["word_count"] = word_counts
    df["text_length"] = df["text"].str.len()
    
    df.to_csv("data.csv", index=False, encoding='utf-8')
    
    print("NLP analizi tamamlandı")
    return df

if __name__ == "__main__":
    nlp_process()
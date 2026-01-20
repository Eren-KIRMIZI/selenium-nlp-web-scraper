import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="Smart Scraper - Advanced Analytics",
    layout="wide"
)

st.title("Smart Scraper - Detaylı Analiz")
st.markdown("*Streamlit ile gelişmiş NLP analizi*")
st.markdown("---")

try:
    df = pd.read_csv("data.csv")
    with open("report.json", encoding='utf-8') as f:
        report = json.load(f)
    data_loaded = True
except FileNotFoundError:
    st.error("Veri bulunamadı! Önce pipeline'ı çalıştır: `python scheduler.py`")
    data_loaded = False

if data_loaded:
    # Metrikler
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Toplam Alıntı", len(df))
    
    with col2:
        st.metric("Yazar Sayısı", df["author"].nunique())
    
    with col3:
        st.metric("Ort. Kelime", round(df["word_count"].mean(), 1))
    
    with col4:
        st.metric("Temizlenen", report["cleaning_results"]["rows_removed"])
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Veri Tablosu", "Grafikler", "NLP Detayları"])
    
    with tab1:
        st.subheader("Toplanan Veriler")
        
        # Filtreleme
        authors = ["Tümü"] + sorted(df["author"].unique().tolist())
        selected_author = st.selectbox("Yazar Filtrele", authors)
        
        filtered_df = df.copy()
        if selected_author != "Tümü":
            filtered_df = filtered_df[filtered_df["author"] == selected_author]
        
        st.write(f"Gösterilen: **{len(filtered_df)}** / {len(df)} alıntı")
        st.dataframe(filtered_df, use_container_width=True, height=400)
        
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("CSV İndir", csv, "data.csv", "text/csv")
    
    with tab2:
        st.subheader("Veri Görselleştirme")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**En Çok Alıntı Yapılan Yazarlar**")
            author_counts = df["author"].value_counts().head(10)
            st.bar_chart(author_counts)
        
        with col2:
            st.write("**Metin Uzunluğu Dağılımı**")
            st.line_chart(df["text_length"])
    
    with tab3:
        st.subheader("NLP Analiz Detayları")
        
        if "entities" in df.columns:
            st.write("**Entity Detection (İlk 10)**")
            entity_df = df[["text", "entities", "author"]].head(10)
            st.dataframe(entity_df, use_container_width=True)
        
        if "pos_tags" in df.columns:
            st.write("**Part-of-Speech Tagging (İlk 10)**")
            pos_df = df[["text", "pos_tags", "word_count"]].head(10)
            st.dataframe(pos_df, use_container_width=True)

st.markdown("---")
st.markdown("**Smart Scraper v1.0** | Selenium + spaCy + Streamlit")
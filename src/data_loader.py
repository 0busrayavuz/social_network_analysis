import pandas as pd
import os
import re

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # URL ve kullanıcı adlarını temizle
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', '', text)
    text = " ".join(text.split())
    return text

def load_data(file_path):
    print(f"Dosya okunuyor: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"Hata: Dosya bulunamadı: {file_path}")
        return None

    df = None
    # Önce noktalı virgül, sonra virgül, en son Excel dene
    try:
        df = pd.read_csv(file_path, sep=';', dtype={'id': str, 'parent_id': str})
        if len(df.columns) < 2: raise ValueError()
    except:
        try:
            df = pd.read_csv(file_path, sep=',', dtype={'id': str, 'parent_id': str})
        except:
            pass
    
    if df is None:
        try:
            df = pd.read_excel(file_path, dtype={'id': str, 'parent_id': str}, engine='openpyxl')
        except:
            print("Hata: Dosya formatı okunamadı.")
            return None

    # Sütun isimlerini düzelt
    df.columns = df.columns.str.strip()
    
    # Eksik verileri doldur
    if 'parent_id' in df.columns: df['parent_id'] = df['parent_id'].fillna("")
    if 'Alt Duygu' in df.columns: df['Alt Duygu'] = df['Alt Duygu'].fillna("Nötr")
    if 'Duygu' in df.columns: df['Duygu'] = df['Duygu'].fillna("Nötr")
    
    # Özel kural: Sitem -> Öfke
    df.loc[df["Alt Duygu"].str.lower() == "sitem", "Alt Duygu"] = "Öfke"

    # Metin temizliği
    if 'text' in df.columns:
        df['clean_text'] = df['text'].apply(clean_text)
    
    print(f"Veri yüklendi: {len(df)} satır.")
    return df
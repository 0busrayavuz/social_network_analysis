import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pyvis.network import Network
import numpy as np
import math
from collections import Counter

# --- KESİN VE NET RENK TABLOSU (REFERANS ALINAN) ---
COLOR_PALETTE = {
    # --- POZİTİF GRUBU ---
    "Pozitif": "#2ecc71",   # Yeşil
    "Empati": "#f5a9b8",    # Pembe (Senin tablodaki gibi)
    "Neşe": "#f1c40f",      # Sarı
    "Umut": "#f39c12",      # Turuncu

    # --- NEGATİF GRUBU ---
    "Negatif": "#e74c3c",   # Kırmızı
    "Öfke": "#c0392b",      # Koyu Kırmızı
    "İğrenme": "#27ae60",   # Koyu Yeşil
    "Umutsuzluk": "#2c3e50",# Koyu Lacivert (Tablona uygun)
    "Suçlama": "#e67e22",   # Turuncu/Kahve
    "Şok": "#8e44ad",       # Mor
    "Üzüntü": "#2980b9",    # Mavi
    "Korku": "#9b59b6",     # Açık Mor
    
    # --- NÖTR GRUBU ---
    "Nötr": "#95a5a6",      # Gri
    "Şaşkınlık": "#16a085", # Turkuaz (Nötr/Negatif geçişli)
    
    # --- DİĞER ---
    "Diğer": "#bdc3c7"      # Açık Gri
}

def get_color(emotion_name):
    """Duygu adına göre renk getirir, yoksa gri döner."""
    if not isinstance(emotion_name, str): return COLOR_PALETTE["Diğer"]
    # Temizlik: Boşlukları sil, baş harfi büyüt
    clean_name = emotion_name.strip().capitalize()
    
    # Özel düzeltmeler (Veri setindeki yazım farkları için)
    if clean_name == "Sitem": return COLOR_PALETTE["Öfke"]
    
    return COLOR_PALETTE.get(clean_name, COLOR_PALETTE["Diğer"])

# --- 1. DERECE DAĞILIMI ---
def plot_degree_distribution(G, output_path):
    print("Grafik çiziliyor: Derece Dağılımı")
    degrees = [d for n, d in G.degree()]
    degree_counts = Counter(degrees)
    unique_seq = sorted(degree_counts.items())
    
    k = np.array([item[0] for item in unique_seq])
    freq = np.array([item[1] for item in unique_seq])
    prob = freq / freq.sum()

    plt.figure(figsize=(8, 6))
    plt.bar(k, prob, color="#2c3e50", alpha=0.9, width=0.8)
    plt.title("Derece Dağılımı (Olasılık)", fontsize=14, fontweight='bold')
    plt.xlabel("Derece")
    plt.ylabel("Olasılık")
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

# --- 2. TEMEL DUYGU GRAFİKLERİ ---
def plot_basic_emotions(df, output_dir):
    print("Grafik çiziliyor: Temel Duygular")
    valid_emotions = ["Pozitif", "Negatif", "Nötr"]
    temp_df = df.copy()
    temp_df["Duygu"] = temp_df["Duygu"].astype(str).str.strip().str.capitalize()
    temp_df.loc[~temp_df["Duygu"].isin(valid_emotions), "Duygu"] = "Nötr"
    
    counts = temp_df["Duygu"].value_counts()
    colors = [get_color(e) for e in counts.index]

    # Bar Grafik
    plt.figure(figsize=(8, 6))
    bars = plt.bar(counts.index, counts.values, color=colors, width=0.6)
    plt.title("Temel Duygu Dağılımı", fontsize=14, fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), int(bar.get_height()), ha='center', va='bottom')
    plt.savefig(f"{output_dir}/temel_duygu_bar.png", dpi=300)
    plt.close()
    
    # Pasta Grafik (Sadece Yüzdeler, Yazı Yok)
    plt.figure(figsize=(8, 6))
    wedges, texts, autotexts = plt.pie(
        counts, 
        autopct="%1.1f%%", 
        colors=colors, 
        startangle=140, 
        explode=[0.02]*len(counts),
        textprops={'color': 'white', 'weight': 'bold', 'fontsize': 11}
    )
    for t in texts: t.set_visible(False) # İsimleri gizle
    
    plt.legend(wedges, counts.index, title="Duygular", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title("Temel Duygu Dağılımı (Oran)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/temel_duygu_pasta.png", dpi=300)
    plt.close()

# --- 3. ALT DUYGU GRAFİKLERİ ---
def plot_sub_emotions_by_sentiment(df, sentiment, output_dir):
    print(f"Grafik çiziliyor: {sentiment} Alt Duygular")
    temp_df = df.copy()
    temp_df["Duygu"] = temp_df["Duygu"].astype(str).str.strip().str.capitalize()
    temp_df["Alt Duygu"] = temp_df["Alt Duygu"].astype(str).str.strip().str.capitalize()
    
    # Sitem -> Öfke dönüşümü
    temp_df.loc[temp_df["Alt Duygu"] == "Sitem", "Alt Duygu"] = "Öfke"
    
    sub_df = temp_df[temp_df["Duygu"] == sentiment.strip().capitalize()]
    if len(sub_df) == 0: return

    counts = sub_df["Alt Duygu"].value_counts()
    colors = [get_color(e) for e in counts.index]
    
    # Bar Grafik
    plt.figure(figsize=(10, 6))
    bars = plt.bar(counts.index, counts.values, color=colors)
    plt.title(f"{sentiment} İçeriklerin Alt Duygu Kırılımı", fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{sentiment.lower()}_alt_duygu_bar.png", dpi=300)
    plt.close()
    
    # Pasta Grafik (Temiz ve Lejantlı)
    plt.figure(figsize=(9, 6))
    wedges, texts, autotexts = plt.pie(
        counts, 
        autopct='%1.1f%%', 
        colors=colors,
        startangle=90,
        pctdistance=0.85,
        explode=[0.02]*len(counts),
        textprops={'fontsize': 9}
    )
    for t in texts: t.set_visible(False) # İsimleri gizle, lejant var
    
    plt.title(f"{sentiment} Alt Duygu Dağılımı", fontsize=14, fontweight='bold')
    plt.legend(wedges, counts.index, title="Alt Duygular", loc="center left", bbox_to_anchor=(1.0, 0.5))
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{sentiment.lower()}_alt_duygu_pasta.png", dpi=300)
    plt.close()

# --- 4. TOPLULUK ANALİZİ ---
def plot_community_analysis(G, community_map, df, output_dir):
    print("Grafik çiziliyor: Topluluk Analizleri")
    df['community'] = df['id'].astype(str).map(community_map)
    
    top_comms = df['community'].value_counts().head(5).index
    df_top = df[df['community'].isin(top_comms)].copy()
    
    df_top["Duygu"] = df_top["Duygu"].astype(str).str.strip().str.capitalize()
    
    pivot = df_top.groupby(['community', 'Duygu']).size().unstack(fill_value=0)
    # Sadece renk paletinde olan sütunları al (Hata önleyici)
    valid_cols = [c for c in pivot.columns if c in COLOR_PALETTE]
    pivot = pivot[valid_cols]
    
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0)
    colors = [get_color(c) for c in pivot.columns]
    
    pivot_pct.plot(kind='bar', stacked=True, color=colors, figsize=(10, 6), width=0.7)
    plt.title("En Büyük 5 Topluluğun Duygu Dağılımı", fontsize=14, fontweight='bold')
    plt.ylabel("Oran")
    plt.xlabel("Topluluk ID")
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', title="Duygular")
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    plt.tight_layout()
    plt.savefig(f"{output_dir}/topluluk_temel_duygu.png", dpi=300)
    plt.close()

# --- 5. RADIAL AĞ (LEJANTLI) ---
def create_radial_network(G, df, output_path):
    print("Ağ oluşturuluyor: Radial Network")
    net = Network(height="850px", width="100%", bgcolor="#ffffff", font_color="#333", select_menu=True)
    
    id_map = df.set_index('id')[['userName', 'text', 'Alt Duygu']].to_dict('index')
    
    roots = [n for n in G.nodes() if G.in_degree(n) == 0]
    spacing = 900
    cols = int(math.ceil(math.sqrt(len(roots))))
    root_pos = {}
    for i, root in enumerate(roots):
        r, c = i // cols, i % cols
        root_pos[root] = (c * spacing, r * spacing)

    used_emotions = set()

    for node in G.nodes():
        data = id_map.get(node, {})
        user = data.get('userName', 'Bilinmiyor')
        text = str(data.get('text', ''))[:60]
        
        raw_emotion = str(data.get('Alt Duygu', 'Nötr')).strip().capitalize()
        if raw_emotion == "Sitem": raw_emotion = "Öfke" # Düzeltme
        
        color = get_color(raw_emotion)
        used_emotions.add(raw_emotion)
        
        if node in root_pos:
            x, y = root_pos[node]
            size = 40
            shape = "dot"
            border_color = "#2c3e50"
        else:
            parents = list(G.predecessors(node))
            if parents and parents[0] in root_pos:
                px, py = root_pos[parents[0]]
                angle = np.random.uniform(0, 2*math.pi)
                radius = np.random.uniform(150, 400)
                x, y = px + radius*math.cos(angle), py + radius*math.sin(angle)
            else:
                x, y = 0, 0
            size = 15
            shape = "dot"
            border_color = color

        title = f"<b>{user}</b><br>{raw_emotion}<br><i>{text}...</i>"
        net.add_node(str(node), label=" ", title=title, color={'background': color, 'border': border_color}, 
                     size=size, shape=shape, x=x, y=y, physics=False, borderWidth=1)
        
    for u, v in G.edges():
        net.add_edge(str(u), str(v), color="#bdc3c7")
        
    net.toggle_physics(False)
    net.save_graph(output_path)
    
    # HTML Lejant Kutusu
    legend_html = """
    <div style="position: fixed; bottom: 20px; left: 20px; background-color: rgba(255,255,255,0.95); 
    border: 1px solid #ccc; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); font-family: Arial, sans-serif;">
      <div style="font-weight: bold; margin-bottom: 10px; text-align: center; border-bottom: 1px solid #ddd; padding-bottom: 5px;">Duygu Renkleri</div>
    """
    for emo in sorted(used_emotions):
        col = get_color(emo)
        legend_html += f'<div style="margin-bottom: 5px;"><span style="background:{col}; width:12px; height:12px; display:inline-block; margin-right:8px; border-radius: 50%;"></span>{emo}</div>'
    legend_html += "</div></body>"
    
    with open(output_path, "r", encoding="utf-8") as f:
        html = f.read()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html.replace("</body>", legend_html))
    
    print(f"Dosya kaydedildi: {output_path}")
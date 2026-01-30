import os
import shutil
from src.data_loader import load_data
from src.analysis import build_graph, detect_communities, calculate_metrics
from src.visualization import (
    plot_degree_distribution,
    plot_basic_emotions,
    plot_sub_emotions_by_sentiment,
    plot_community_analysis,
    create_radial_network
)

DATA_FILE = "data/EmpaTech-data-set.csv"
OUTPUT_DIR = "outputs"
PLOTS_DIR = os.path.join(OUTPUT_DIR, "plots")
REPORT_DIR = os.path.join(OUTPUT_DIR, "reports")

def clean_previous_outputs():
    if os.path.exists(OUTPUT_DIR):
        print("Eski çıktılar temizleniyor...")
        shutil.rmtree(OUTPUT_DIR)
    
    os.makedirs(PLOTS_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)

def save_report(metrics, num_communities, output_path):
    """Metrikleri txt dosyasına yazar."""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("========================================\n")
            f.write("      EMPATECH SOSYAL AĞ ANALİZİ       \n")
            f.write("========================================\n\n")
            
            f.write("--- GENEL AĞ METRİKLERİ ---\n")
            for key, value in metrics.items():
                f.write(f"{key.ljust(35)}: {value}\n")
            
            f.write(f"\n{'Tespit Edilen Topluluk Sayısı'.ljust(35)}: {num_communities}\n")
            
            f.write("\n========================================\n")
            f.write("Rapor Sonu\n")
        print(f"Rapor dosyaya kaydedildi: {output_path}")
    except Exception as e:
        print(f"Rapor kaydedilirken hata oluştu: {e}")

def main():
    clean_previous_outputs()
    
    print("\nEmpaTech Analizi Başlatılıyor...\n")
    
    # 1. Veri Yükle
    df = load_data(DATA_FILE)
    if df is None: return

    # 2. Ağı Oluştur
    G = build_graph(df)
    
    # 3. Metrikleri Hesapla
    metrics = calculate_metrics(G)
    
    # 4. Toplulukları Bul
    community_map, num_communities = detect_communities(G)
    print(f"\nTespit edilen topluluk sayısı: {num_communities}")

    # --- RAPORU KAYDET ---
    save_report(metrics, num_communities, f"{REPORT_DIR}/Ag_Analiz_Raporu.txt")

    print("\nGrafikler çiziliyor...")
    
    plot_degree_distribution(G, f"{PLOTS_DIR}/1_derece_dagilimi.png")
    plot_basic_emotions(df, PLOTS_DIR)
    plot_sub_emotions_by_sentiment(df, "Pozitif", PLOTS_DIR)
    plot_sub_emotions_by_sentiment(df, "Negatif", PLOTS_DIR)
    plot_community_analysis(G, community_map, df, PLOTS_DIR)
    create_radial_network(G, df, f"{PLOTS_DIR}/EmpaTech_ozel_ag.html")

    print(f"\nİşlem tamamlandı! Sonuçlar '{OUTPUT_DIR}' klasöründe.")

if __name__ == "__main__":
    main()
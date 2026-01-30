import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities

def build_graph(df):
    print("Ağ inşa ediliyor...")
    G = nx.DiGraph()

    for _, row in df.iterrows():
        node_id = str(row['id'])
        G.add_node(node_id, 
                   userName=row.get('userName', 'Bilinmiyor'),
                   text=row.get('text', ''),
                   sub_emotion=row.get('Alt Duygu', 'Nötr'),
                   main_emotion=row.get('Duygu', 'Nötr'))
    
    for _, row in df.iterrows():
        node_id = str(row['id'])
        parent_id = str(row['parent_id'])
        
        if parent_id and parent_id != "nan" and parent_id != "":
            if parent_id in G.nodes:
                G.add_edge(parent_id, node_id)
    
    return G

def calculate_metrics(G):
    print("Metrikler hesaplanıyor...")
    
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    density = nx.density(G)
    
    degrees = [d for n, d in G.degree()]
    avg_degree = sum(degrees) / len(degrees) if degrees else 0

    # Bağlantılı bileşen analizi
    is_connected = nx.is_weakly_connected(G)
    num_components = nx.number_weakly_connected_components(G)
    
    # Çap ve Yol Uzunluğu (Sadece en büyük parça için hesaplanır)
    if num_nodes > 0:
        largest_cc = max(nx.weakly_connected_components(G), key=len)
        subgraph = G.subgraph(largest_cc)
        # Çap hesabı yönlü graflarda zordur, yönsüz kabul ederek yaklaşık hesaplıyoruz
        undirected_sub = subgraph.to_undirected()
        try:
            diameter = nx.diameter(undirected_sub)
            avg_path = nx.average_shortest_path_length(undirected_sub)
        except:
            diameter = "Hesaplanamadı"
            avg_path = "Hesaplanamadı"
    else:
        diameter = 0
        avg_path = 0

    metrics = {
        "Toplam Düğüm": num_nodes,
        "Toplam Kenar": num_edges,
        "Yoğunluk": f"{density:.5f}",
        "Ortalama Derece": f"{avg_degree:.2f}",
        "Bağlantılı Mı": "Evet" if is_connected else "Hayır",
        "Bileşen Sayısı": num_components,
        "Ağ Çapı (En Büyük Parça)": diameter,
        "Ort. Yol Uzunluğu (En Büyük Parça)": f"{avg_path:.2f}" if isinstance(avg_path, float) else avg_path
    }
    
    # Terminale yaz
    for k, v in metrics.items():
        print(f"{k}: {v}")
        
    return metrics

def detect_communities(G):
    print("Topluluk tespiti yapılıyor...")
    G_undirected = G.to_undirected()
    communities = greedy_modularity_communities(G_undirected)
    
    community_map = {}
    for i, community in enumerate(communities):
        for node in community:
            community_map[node] = i
            
    return community_map, len(communities)
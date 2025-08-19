# texas_graph.py
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# ---------------------------
# 1) Data: cities with lat, lon, population (approximate, edit as needed)
#    Feel free to add/remove places or update populations.
# ---------------------------
CITIES = {
    # Big metro cores
    "Houston":          {"lat": 29.7604, "lon": -95.3698, "pop": 2300000},
    "San Antonio":      {"lat": 29.4241, "lon": -98.4936, "pop": 1550000},
    "Dallas":           {"lat": 32.7767, "lon": -96.7970, "pop": 1310000},
    "Austin":           {"lat": 30.2672, "lon": -97.7431, "pop":  975000},
    "Fort Worth":       {"lat": 32.7555, "lon": -97.3308, "pop":  960000},
    "El Paso":          {"lat": 31.7619, "lon":-106.4850, "pop":  680000},
    # Large cities
    "Arlington":        {"lat": 32.7357, "lon": -97.1081, "pop":  400000},
    "Corpus Christi":   {"lat": 27.8006, "lon": -97.3964, "pop":  320000},
    "Plano":            {"lat": 33.0198, "lon":-96.6989, "pop":  290000},
    "Laredo":           {"lat": 27.5306, "lon": -99.4803, "pop":  260000},
    "Lubbock":          {"lat": 33.5779, "lon":-101.8552, "pop": 260000},
    "Garland":          {"lat": 32.9126, "lon": -96.6389, "pop":  240000},
    "Irving":           {"lat": 32.8140, "lon": -96.9489, "pop":  255000},
    "Amarillo":         {"lat": 35.2210, "lon":-101.8313, "pop":  200000},
    "Grand Prairie":    {"lat": 32.7459, "lon": -96.9978, "pop":  200000},
    "Brownsville":      {"lat": 25.9017, "lon": -97.4975, "pop":  190000},
    "McKinney":         {"lat": 33.1972, "lon": -96.6398, "pop":  210000},
    "Frisco":           {"lat": 33.1507, "lon": -96.8236, "pop":  220000},
    "Pasadena":         {"lat": 29.6911, "lon": -95.2091, "pop":  150000},
    "Killeen":          {"lat": 31.1171, "lon": -97.7278, "pop":  160000},
    "Waco":             {"lat": 31.5493, "lon": -97.1467, "pop":  140000},
    "Denton":           {"lat": 33.2148, "lon": -97.1331, "pop":  150000},
    "Midland":          {"lat": 31.9973, "lon":-102.0779, "pop":  135000},
    "Odessa":           {"lat": 31.8457, "lon":-102.3676, "pop":  115000},
    "Round Rock":       {"lat": 30.5083, "lon": -97.6789, "pop":  135000},
    "College Station":  {"lat": 30.6279, "lon": -96.3344, "pop":  120000},
    "Abilene":          {"lat": 32.4487, "lon": -99.7331, "pop":  125000},
    "Beaumont":         {"lat": 30.0802, "lon": -94.1266, "pop":  115000},
    "Tyler":            {"lat": 32.3513, "lon": -95.3011, "pop":  110000},
    "San Angelo":       {"lat": 31.4638, "lon":-100.4370, "pop":  100000},
    # Smaller towns (examples)
    "Nacogdoches":      {"lat": 31.6035, "lon": -94.6555, "pop":   33000},
    "Kerrville":        {"lat": 30.0474, "lon": -99.1403, "pop":   24000},
    "Fredericksburg":   {"lat": 30.2744, "lon": -98.8719, "pop":   12000},
    "Brenham":          {"lat": 30.1669, "lon": -96.3977, "pop":   17500},
    "Alpine":           {"lat": 30.3585, "lon":-103.6610, "pop":    6200},
    "Marfa":            {"lat": 30.3090, "lon":-104.0206, "pop":    1800},
}

# ---------------------------
# 2) Classification rules
#    Choose ONE of these:
#    A) Fixed population threshold
THRESHOLD_POP = 300_000
USE_TOP_K_BIG = False
TOP_K_BIG = 10
# ---------------------------

def classify_cities(cities):
    # A) threshold
    if not USE_TOP_K_BIG:
        big = {name for name, d in cities.items() if d["pop"] >= THRESHOLD_POP}
        small = set(cities.keys()) - big
        return big, small
    # B) top-k biggest
    sorted_names = sorted(cities.keys(), key=lambda n: cities[n]["pop"], reverse=True)
    big = set(sorted_names[:TOP_K_BIG])
    small = set(sorted_names[TOP_K_BIG:])
    return big, small

# Great-circle distance (haversine) in km
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dlambda/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

# ---------------------------
# 3) Build graph
#    Strategy: connect each node to its k nearest neighbors (different k for big vs small).
# ---------------------------
K_NEIGHBORS_BIG = 6
K_NEIGHBORS_SMALL = 3

def build_graph(cities, k_big=K_NEIGHBORS_BIG, k_small=K_NEIGHBORS_SMALL):
    G = nx.Graph()
    for name, d in cities.items():
        G.add_node(name,
                   lat=d["lat"], lon=d["lon"], population=d["pop"])
    big, small = classify_cities(cities)

    names = list(cities.keys())
    # Precompute all pairwise distances
    dist = {}
    for i, u in enumerate(names):
        for j in range(i+1, len(names)):
            v = names[j]
            du = cities[u]; dv = cities[v]
            dkm = haversine_km(du["lat"], du["lon"], dv["lat"], dv["lon"])
            dist[(u, v)] = dist[(v, u)] = dkm

    # For each node, add edges to k nearest neighbors
    for u in names:
        k = k_big if u in big else k_small
        # sort neighbors by distance
        neighbors = sorted([v for v in names if v != u], key=lambda v: dist[(u, v)])
        chosen = neighbors[:k]
        for v in chosen:
            if not G.has_edge(u, v):
                G.add_edge(u, v, distance=round(dist[(u, v)], 1))

    return G, big, small

# ---------------------------
# 4) Draw
# ---------------------------
def draw_graph(G, big, small, title="Texas network"):
    # Use lon, lat for plotting (simple plan view; not a projection)
    pos = {n: (G.nodes[n]["lon"], G.nodes[n]["lat"]) for n in G.nodes}

    # Style: big cities vs towns (size can be uniform if you prefer)
    node_sizes = [220 if n in big else 150 for n in G.nodes]
    node_colors = ["red" if n in big else "skyblue" for n in G.nodes]

    plt.figure(figsize=(12, 10))
    # Draw only connections (no edge labels)
    nx.draw_networkx_edges(G, pos, width=0.9, alpha=0.7)

    # Draw only nodes (no population scaling shown)
    nx.draw_networkx_nodes(
        G, pos,
        node_size=node_sizes,
        node_color=node_colors,
        edgecolors="black",
        linewidths=0.8,
        alpha=0.95
    )

    # Draw only city names (no population in label)
    nx.draw_networkx_labels(G, pos, font_size=8)

    plt.title(title, fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

def save_matrices(G, filename_prefix="texas"):
    nodes = list(G.nodes)
    n = len(nodes)
    
    # Adjacency matrix (binary)
    A = np.zeros((n, n), dtype=int)
    # Weight matrix (distances) — optional, keep for optimization
    W = np.full((n, n), np.inf)

    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if i == j:
                A[i, j] = 1
                W[i, j] = 0
            elif G.has_edge(u, v):
                A[i, j] = 1
                W[i, j] = G[u][v]["distance"]

    # Save as CSV
    np.savetxt(f"{filename_prefix}_adjacency.csv", A, fmt="%d", delimiter=",")
    np.savetxt(f"{filename_prefix}_weights.csv", W, fmt="%.2f", delimiter=",")

    print(f"Saved adjacency → {filename_prefix}_adjacency.csv")
    print(f"Saved weights   → {filename_prefix}_weights.csv")


# ---------------------------
# 5) Run
# ---------------------------
if __name__ == "__main__":
    G, big, small = build_graph(CITIES)
    print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
    print(f"Big cities ({len(big)}): {sorted(big)}")
    print(f"Towns ({len(small)}): {len(small)}")
    draw_graph(G, big, small)
    save_matrices(G)

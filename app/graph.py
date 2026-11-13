"""Road graph of Bengaluru landmarks and a Dijkstra router (distance or time optimised)."""
import heapq
from math import asin, cos, radians, sin, sqrt

PLACES = {
    "MG Road": (12.9756, 77.6066), "Indiranagar": (12.9784, 77.6408), "Koramangala": (12.9352, 77.6245),
    "HSR Layout": (12.9116, 77.6474), "Whitefield": (12.9698, 77.7500), "Electronic City": (12.8399, 77.6770),
    "Majestic": (12.9767, 77.5713), "Malleshwaram": (13.0031, 77.5643), "Hebbal": (13.0358, 77.5970),
    "Jayanagar": (12.9250, 77.5938), "Marathahalli": (12.9591, 77.6974), "Airport": (13.1989, 77.7068),
}
# (a, b, avg speed km/h): speed models traffic on that stretch
ROADS = [
    ("MG Road", "Indiranagar", 22), ("MG Road", "Majestic", 18), ("MG Road", "Koramangala", 20),
    ("Indiranagar", "Marathahalli", 25), ("Marathahalli", "Whitefield", 28), ("Indiranagar", "Koramangala", 18),
    ("Koramangala", "HSR Layout", 24), ("HSR Layout", "Electronic City", 35), ("Koramangala", "Jayanagar", 20),
    ("Jayanagar", "Majestic", 18), ("Majestic", "Malleshwaram", 20), ("Malleshwaram", "Hebbal", 26),
    ("Hebbal", "Airport", 55), ("Hebbal", "MG Road", 22), ("Marathahalli", "HSR Layout", 22),
    ("Whitefield", "Airport", 40),
]


def haversine_km(a: tuple, b: tuple) -> float:
    lat1, lon1, lat2, lon2 = map(radians, (*a, *b))
    h = sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) * sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371 * asin(sqrt(h))


def build_graph(closed: set[frozenset] = frozenset()) -> dict:
    graph = {p: [] for p in PLACES}
    for a, b, speed in ROADS:
        if frozenset((a, b)) in closed:
            continue
        km = haversine_km(PLACES[a], PLACES[b])
        edge = {"km": km, "min": km / speed * 60}
        graph[a].append((b, edge))
        graph[b].append((a, edge))
    return graph


def shortest_path(src: str, dst: str, optimise: str = "time", closed: set[frozenset] = frozenset()):
    if src not in PLACES or dst not in PLACES:
        raise KeyError("Unknown place")
    weight = "min" if optimise == "time" else "km"
    graph = build_graph(closed)
    best = {src: 0.0}
    prev: dict[str, str] = {}
    queue = [(0.0, src)]
    while queue:
        cost, node = heapq.heappop(queue)
        if node == dst:
            break
        if cost > best.get(node, float("inf")):
            continue
        for nxt, edge in graph[node]:
            new = cost + edge[weight]
            if new < best.get(nxt, float("inf")):
                best[nxt], prev[nxt] = new, node
                heapq.heappush(queue, (new, nxt))
    if dst not in best:
        return None
    path = [dst]
    while path[-1] != src:
        path.append(prev[path[-1]])
    path.reverse()
    km = sum(haversine_km(PLACES[a], PLACES[b]) for a, b in zip(path, path[1:]))
    minutes = sum(next(e["min"] for n, e in graph[a] if n == b) for a, b in zip(path, path[1:]))
    return {"path": path, "distance_km": round(km, 2), "eta_min": round(minutes), "optimise": optimise}

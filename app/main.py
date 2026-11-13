"""RouteWise: a maps route-finder API on top of a Dijkstra engine."""
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

from .graph import PLACES, ROADS, shortest_path

app = FastAPI(title="RouteWise")
STATIC = Path(__file__).parent / "static"
_closed: set[frozenset] = set()


def reset_state():
    _closed.clear()


@app.get("/")
def home():
    return FileResponse(STATIC / "index.html")


@app.get("/api/places")
def places():
    return [{"name": n, "lat": lat, "lng": lng} for n, (lat, lng) in PLACES.items()]


@app.get("/api/route")
def route(src: str = Query(alias="from"), dst: str = Query(alias="to"), optimise: str = "time"):
    if optimise not in ("time", "distance"):
        raise HTTPException(422, "optimise must be time or distance")
    if src == dst:
        raise HTTPException(422, "Start and destination are the same")
    try:
        result = shortest_path(src, dst, optimise, _closed)
    except KeyError:
        raise HTTPException(404, "Unknown place")
    if result is None:
        raise HTTPException(404, "No route available")
    result["coords"] = [PLACES[p] for p in result["path"]]
    return result


@app.post("/api/closures")
def close_road(a: str, b: str):
    if not any({a, b} == {x, y} for x, y, _ in ROADS):
        raise HTTPException(404, "No such road")
    _closed.add(frozenset((a, b)))
    return {"closed": sorted(map(sorted, _closed))}


@app.delete("/api/closures")
def reopen_all():
    reset_state()
    return {"closed": []}

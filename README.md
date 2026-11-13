# 🗺️ RouteWise — Maps Route Finder

![CI](https://github.com/Sandesh7777777/routewise-maps/actions/workflows/ci.yml/badge.svg)

A Google-Maps-style route finder for Bengaluru: pick two places and get the **fastest** or **shortest** route on a live Leaflet map, with ETA and road-closure rerouting.

## Features
- Dijkstra shortest-path engine, optimising for time (traffic-aware speeds) or distance
- Haversine distances from real coordinates
- Road closures that reroute traffic, and a clean 404 when a place becomes unreachable
- Leaflet + OpenStreetMap map with markers and the route drawn as a polyline

## Tech
FastAPI · Leaflet · **Pytest** · **Playwright** · GitHub Actions

## Test strategy
| Layer | File | What it proves |
|---|---|---|
| Unit | `tests/test_graph_unit.py` | haversine accuracy and symmetry, path integrity, and **property checks across all 132 place pairs**: shortest-distance route is never longer, fastest route is never slower |
| API | `tests/test_route_api.py` | route payload contract, closure rerouting, unreachable destinations, parametrized negatives |
| UI E2E | `tests/test_route_ui.py` | user journey and error messaging in Chromium |

## Run
```bash
pip install -r requirements.txt
python -m playwright install chromium
uvicorn app.main:app --reload     # open http://127.0.0.1:8000
pytest
```

Built by **Sandesh Pande** · SDET / AI Test Automation Engineer

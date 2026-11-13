import pytest


@pytest.mark.api
def test_lists_twelve_places(api):
    assert len(api.get("/api/places").json()) == 12


@pytest.mark.api
def test_route_has_path_distance_eta_and_coords(api):
    body = api.get("/api/route", params={"from": "Majestic", "to": "Whitefield"}).json()
    assert body["path"][0] == "Majestic" and body["path"][-1] == "Whitefield"
    assert body["distance_km"] > 0 and body["eta_min"] > 0
    assert len(body["coords"]) == len(body["path"])


@pytest.mark.api
def test_road_closure_reroutes(api):
    before = api.get("/api/route", params={"from": "Hebbal", "to": "Airport"}).json()
    assert before["path"] == ["Hebbal", "Airport"]
    api.post("/api/closures", params={"a": "Hebbal", "b": "Airport"})
    after = api.get("/api/route", params={"from": "Hebbal", "to": "Airport"}).json()
    assert after["path"][-2] == "Whitefield"
    assert after["eta_min"] > before["eta_min"]


@pytest.mark.api
def test_isolated_destination_returns_404(api):
    for a, b in [("Hebbal", "Airport"), ("Whitefield", "Airport")]:
        api.post("/api/closures", params={"a": a, "b": b})
    r = api.get("/api/route", params={"from": "MG Road", "to": "Airport"})
    assert r.status_code == 404 and r.json()["detail"] == "No route available"


@pytest.mark.api
@pytest.mark.parametrize("params,status", [
    ({"from": "Mars", "to": "Hebbal"}, 404),
    ({"from": "Hebbal", "to": "Hebbal"}, 422),
    ({"from": "Hebbal", "to": "Airport", "optimise": "scenic"}, 422),
    ({"from": "Hebbal"}, 422),
], ids=["unknown-place", "same-place", "bad-mode", "missing-to"])
def test_invalid_route_requests(api, params, status):
    assert api.get("/api/route", params=params).status_code == status


@pytest.mark.api
def test_closing_a_non_existent_road_is_404(api):
    assert api.post("/api/closures", params={"a": "Hebbal", "b": "Electronic City"}).status_code == 404

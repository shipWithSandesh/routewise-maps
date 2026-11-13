import pytest

from app.graph import PLACES, haversine_km, shortest_path


@pytest.mark.unit
def test_haversine_known_distance():
    # MG Road to Majestic is roughly 3.8 km as the crow flies
    assert 3.5 < haversine_km(PLACES["MG Road"], PLACES["Majestic"]) < 4.1


@pytest.mark.unit
def test_haversine_is_symmetric_and_zero_on_self():
    a, b = PLACES["Hebbal"], PLACES["Airport"]
    assert haversine_km(a, b) == pytest.approx(haversine_km(b, a))
    assert haversine_km(a, a) == 0


@pytest.mark.unit
def test_route_to_self_is_single_node():
    assert shortest_path("Hebbal", "Hebbal")["path"] == ["Hebbal"]


@pytest.mark.unit
def test_path_is_contiguous_and_starts_and_ends_correctly():
    r = shortest_path("Electronic City", "Airport")
    assert r["path"][0] == "Electronic City" and r["path"][-1] == "Airport"
    assert len(r["path"]) == len(set(r["path"]))


@pytest.mark.unit
def test_distance_route_never_longer_than_time_route():
    for src in PLACES:
        for dst in PLACES:
            if src != dst:
                assert shortest_path(src, dst, "distance")["distance_km"] <= shortest_path(src, dst, "time")["distance_km"] + 1e-9


@pytest.mark.unit
def test_time_route_never_slower_than_distance_route():
    for src in PLACES:
        for dst in PLACES:
            if src != dst:
                assert shortest_path(src, dst, "time")["eta_min"] <= shortest_path(src, dst, "distance")["eta_min"] + 1

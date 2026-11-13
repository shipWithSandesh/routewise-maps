import pytest
from playwright.sync_api import Page, expect


@pytest.mark.ui
def test_user_finds_fastest_route_to_airport(page: Page, live_server):
    page.goto(live_server)
    page.get_by_label("From").select_option("Koramangala")
    page.get_by_label("To").select_option("Airport")
    page.get_by_role("button", name="Find route").click()
    expect(page.get_by_test_id("result")).to_contain_text("km")
    expect(page.locator("#path")).to_contain_text("Koramangala")
    expect(page.locator("#path")).to_contain_text("Airport")


@pytest.mark.ui
def test_same_start_and_end_shows_error(page: Page, live_server):
    page.goto(live_server)
    page.get_by_label("From").select_option("Hebbal")
    page.get_by_label("To").select_option("Hebbal")
    page.get_by_role("button", name="Find route").click()
    expect(page.get_by_test_id("error")).to_have_text("Start and destination are the same")

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.dashboard_page import DashboardPage

# Simulated expected values from logic
expected_values = {
    "A": {"load": 120.0, "status": "OVERLOAD"},
    "B": {"load": 80.0, "status": "OK"},
    "C": {"load": 95.0, "status": "OVERLOAD"},
    "D": {"load": 40.0, "status": "OK"}
}

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("file://" + __import__("os").path.abspath("dashboard.html"))
    yield driver
    driver.quit()

def test_dashboard_zones(driver):
    dashboard = DashboardPage(driver)

    for zone, expected in expected_values.items():
        load = dashboard.get_zone_load(zone)
        status_text, status_class = dashboard.get_zone_status(zone)

        assert load == expected["load"], f"{zone} load mismatch"
        assert expected["status"] in status_text, f"{zone} status text mismatch"
        if expected["status"] == "OVERLOAD":
            assert "overload" in status_class
        else:
            assert "ok" in status_class

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dash_application_updatedVer import app

def test_header_present(dash_duo):
    dash_duo.start_server(app)
    header = dash_duo.find_element("h1")
    assert header.is_displayed()
    assert "Pink Morsels Sales Report" in header.text

def test_visualization_present(dash_duo):
    dash_duo.start_server(app)
    WebDriverWait(dash_duo.driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#sales-graph svg"))
    )
    graph_container = dash_duo.find_element("#sales-graph")
    assert graph_container.is_displayed()

def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)
    radio_container = dash_duo.find_element("#region-radio")
    options = radio_container.find_elements(By.TAG_NAME, "input")
    labels = [label.text for label in radio_container.find_elements(By.TAG_NAME, "label")]
    expected_labels = {"All", "North", "South", "East", "West"}
    found_labels = set(label.strip() for label in labels if label.strip())
    assert len(options) == 5
    assert expected_labels.issubset(found_labels)
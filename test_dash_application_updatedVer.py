import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dash_application_updatedVer import app

def test_header_present(dash_duo): 
    """check main header (h1) displays with right title"""
    dash_duo.start_server(app)   #Start the app server for testing
    header = dash_duo.find_element("h1")
    assert header.is_displayed()
    assert "Pink Morsels Sales Report" in header.text

def test_visualization_present(dash_duo):
    """Verify the sales graph with id 'sales-graph is shown"""
    dash_duo.start_server(app)   #wait fo 5 seconds for the graph's SVG element to be visible
    WebDriverWait(dash_duo.driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#sales-graph svg"))
    )
    graph_container = dash_duo.find_element("#sales-graph")   #Locate the container element that holds the sales graph
    assert graph_container.is_displayed()   #Assert the fraph_container is visible

def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)
    radio_container = dash_duo.find_element("#region-radio")   #Find the radio button group container for the region selection
    options = radio_container.find_elements(By.TAG_NAME, "input")
    labels = [label.text for label in radio_container.find_elements(By.TAG_NAME, "label")]
    expected_labels = {"All", "North", "South", "East", "West"}
    found_labels = set(label.strip() for label in labels if label.strip())
    assert len(options) == 5   #Confirm all the expected region labels are included in the found labels
    assert expected_labels.issubset(found_labels)

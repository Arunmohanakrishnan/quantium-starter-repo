import pytest
from dash.testing.application_runners import import_app


@pytest.fixture
def app():
    return import_app("app")


def test_header_is_present(dash_duo, app):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("h1", timeout=10)
    header = dash_duo.find_element("h1")
    assert header is not None
    assert "Soul Foods" in header.text


def test_chart_is_present(dash_duo, app):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-chart", timeout=10)
    chart = dash_duo.find_element("#sales-chart")
    assert chart is not None


def test_region_picker_is_present(dash_duo, app):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-filter", timeout=10)
    region_filter = dash_duo.find_element("#region-filter")
    assert region_filter is not None
    inputs = dash_duo.driver.find_elements("css selector", "#region-filter input[type='radio']")
    assert len(inputs) == 5

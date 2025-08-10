from unittest.mock import patch, Mock
import pytest

from src.collect import geocode, current_weather

def test_geocode_success():
    fake = {"results": [{"latitude": 51.5, "longitude": -0.12, "name": "London"}]}
    with patch("requests.get", return_value=Mock(status_code=200, json=lambda: fake, raise_for_status=lambda: None)):
        lat, lon, name = geocode("London")
        assert name == "London"
        assert lat == 51.5

def test_geocode_no_results():
    fake = {"results": []}
    with patch("requests.get", return_value=Mock(status_code=200, json=lambda: fake, raise_for_status=lambda: None)):
        with pytest.raises(RuntimeError):
            geocode("NowhereVille")

def test_current_weather_success():
    fake = {"current_weather": {"temperature": 18.3, "windspeed": 2.1, "winddirection": 230, "weathercode": 3}}
    with patch("requests.get", return_value=Mock(status_code=200, json=lambda: fake, raise_for_status=lambda: None)):
        cur = current_weather(51.5, -0.12)
        assert cur["temperature"] == 18.3

def test_current_weather_missing_key():
    fake = {}
    with patch("requests.get", return_value=Mock(status_code=200, json=lambda: fake, raise_for_status=lambda: None)):
        with pytest.raises(RuntimeError):
            current_weather(51.5, -0.12)

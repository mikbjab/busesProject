import datetime

import pandas as pd

import pytest
from unittest.mock import patch
from transportanalysis.download import DataRetrieval


@pytest.fixture(scope="module")
def data_retrieval_instance():
    return DataRetrieval()


def test_collect_bus_location(data_retrieval_instance):
    # Assuming API request is mocked, so testing behavior when response is 200
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"result": [{"test_data": "test_value"}]}
        data_retrieval_instance.collect_bus_location(0)

    # Verify if the file is created
    data_path = data_retrieval_instance.project_path.joinpath("data")
    assert data_path.joinpath(f"data{datetime.datetime.now().strftime('_%Y-%m-%d.json')}").exists()


def test_collect_busstops_location(data_retrieval_instance):
    # Assuming API request is mocked, so testing behavior when response is 200
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"result": [{"values":[{"key":"test_key","value":"test_value"}]}]}
        data_retrieval_instance.collect_busstops_location()

    # Verify if the file is created
    data_path = data_retrieval_instance.project_path.joinpath("data")
    assert data_path.joinpath(f"stops_locations{datetime.datetime.now().strftime('_%Y-%m-%d.json')}").exists()


def test_collect_schedule_single(data_retrieval_instance):
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"result": [{"values": [{"value": "123"}]}]}
        schedule_frame = data_retrieval_instance.collect_schedule_single("123", "456", "789")
        assert schedule_frame.iloc[0]["zespol"] == "123"
        assert schedule_frame.iloc[0]["slupek"] == "456"
        assert schedule_frame.iloc[0]["linia"] == "789"
# Similar tests can be written for other methods like collect_lines_single, collect_lines_all,
# collect_schedule_single, collect_schedule_all, find_latest_file

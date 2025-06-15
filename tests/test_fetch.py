from fetch import fetch_post_ids
from unittest.mock import patch, Mock
import requests
import pytest

@patch("fetch.requests.get")
def test_fetch_post_ids_response(mock_get):
    fake_post_ids = list(range(123456, 123466))
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_post_ids
    mock_get.return_value = mock_response

    result = fetch_post_ids(limit=3)
    assert result == fake_post_ids[:3]


@patch("fetch.requests.get")
def test_fetch_post_ids(mock_get):
    fake_post_ids = list(range(123456, 123466))
    
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = fake_post_ids

    # Make raise_for_status() simulate a failure
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(f"{mock_response.status_code} Server Error")
    
    mock_get.return_value = mock_response

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_post_ids(limit=3)


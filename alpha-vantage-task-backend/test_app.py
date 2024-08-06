import pytest
from flask import jsonify
from unittest.mock import Mock
from app import app, RESOURCE_INTERVALS, Cache
import requests
from utils import calculate_daily_average, print_api_data

# Mock the Cache object
app.config['CACHE_TYPE'] = 'null'
Cache(app)

@pytest.fixture
def client():
    # Fixture to create a test client for the Flask app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test case: Ensure the API returns an error when dates are missing
def test_daily_average_missing_dates(client):
    # Send a GET request without start_date and end_date
    response = client.get('/daily_average?function=WTI')
    
    # Assert that the response has a 400 status code and the correct error message
    assert response.status_code == 400
    assert "Start date and end date are required" in response.json['error']

# Test case: Verify that the API handles invalid function (resource) correctly
def test_daily_average_invalid_function(client):
    # Send a GET request with an invalid function
    response = client.get('/daily_average?function=INVALID&start_date=2023-01-01&end_date=2023-12-31')
    
    # Assert that the response has a 400 status code and the correct error message
    assert response.status_code == 400
    assert "Invalid resource: INVALID" in response.json['error']

# Test case: Check if the API returns correct data for a valid request
def test_daily_average_valid_request(client, mocker):
    # Mock data to simulate API response
    mock_data = {
        "data": [
            {"date": "2023-01-01", "value": "70"},
            {"date": "2023-01-02", "value": "72"},
            {"date": "2023-01-03", "value": "75"},
        ]
    }
    # Mock the requests.get function to return our mock data
    mocker.patch('requests.get', return_value=mocker.Mock(json=lambda: mock_data))
    
    # Send a GET request with valid parameters
    response = client.get('/daily_average?function=WTI&start_date=2023-01-01&end_date=2023-01-03')
    
    # Assert that the response is correct
    assert response.status_code == 200
    assert response.json['function'] == 'WTI'
    assert response.json['average_price'] == 72.33
    assert response.json['currency'] == 'USD per unit'

# Test case: Verify the calculate_daily_average function works correctly
def test_calculate_daily_average():
    # Sample data for testing
    data = {
        "data": [
            {"date": "2023-01-01", "value": "70"},
            {"date": "2023-01-02", "value": "72"},
            {"date": "2023-01-03", "value": "75"},
        ]
    }
    # Calculate the average using our function
    average = calculate_daily_average(data, "2023-01-01", "2023-01-03")
    
    # Assert that the calculated average is correct
    assert round(average, 2) == 72.33

# Test case: Ensure calculate_daily_average returns None for empty date range
def test_calculate_daily_average_empty_range():
    # Sample data for testing
    data = {
        "data": [
            {"date": "2023-01-01", "value": "70"},
            {"date": "2023-01-02", "value": "72"},
            {"date": "2023-01-03", "value": "75"},
        ]
    }
    # Calculate average for a date range with no data
    average = calculate_daily_average(data, "2023-01-04", "2023-01-05")
    
    # Assert that the function returns None for an empty range
    assert average is None

# Test case: Check if print_api_data function outputs correct information
def test_print_api_data(capsys):
    # Sample data for testing
    data = {
        "data": [
            {"date": "2023-01-01", "value": "70"},
            {"date": "2023-01-02", "value": "72"},
            {"date": "2023-01-03", "value": "75"},
        ]
    }
    # Call the print_api_data function
    print_api_data(data, "2023-01-01", "2023-01-03")
    
    # Capture the printed output
    captured = capsys.readouterr()
    
    # Assert that the correct information was printed
    assert "API Data Summary:" in captured.out
    assert "Total data points: 3" in captured.out

# Test case: Verify API handles different intervals correctly
def test_daily_average_different_intervals(client, mocker):
    # Mock data to simulate API response for weekly interval
    mock_data = {
        "data": [
            {"date": "2023-01-01", "value": "70"},
            {"date": "2023-01-08", "value": "72"},
            {"date": "2023-01-15", "value": "75"},
        ]
    }
    # Mock the requests.get function to return our mock data
    mocker.patch('requests.get', return_value=mocker.Mock(json=lambda: mock_data))
    
    # Send a GET request with weekly interval
    response = client.get('/daily_average?function=WTI&interval=weekly&start_date=2023-01-01&end_date=2023-01-15')
    
    # Assert that the response is correct for weekly interval
    assert response.status_code == 200
    assert response.json['interval'] == 'weekly'
    assert response.json['average_price'] == 72.33

# Test case: Check if API returns error for invalid interval
def test_daily_average_invalid_interval(client):
    # Send a GET request with an invalid interval
    response = client.get('/daily_average?function=WTI&interval=invalid&start_date=2023-01-01&end_date=2023-12-31')
    
    # Assert that the response has a 400 status code and the correct error message
    assert response.status_code == 400
    assert "Invalid interval 'invalid' for resource 'WTI'" in response.json['error']

# Test case: Ensure API returns error when start date is missing
def test_daily_average_missing_start_date(client):
    # Send a GET request without start_date
    response = client.get('/daily_average?function=WTI&interval=daily&end_date=2023-12-31')
    
    # Assert that the response has a 400 status code and the correct error message
    assert response.status_code == 400
    assert "Start date and end date are required" in response.json['error']

# Test case: Verify API returns error when end date is missing
def test_daily_average_missing_end_date(client):
    # Send a GET request without end_date
    response = client.get('/daily_average?function=WTI&interval=daily&start_date=2023-01-01')
    
    # Assert that the response has a 400 status code and the correct error message
    assert response.status_code == 400
    assert "Start date and end date are required" in response.json['error']

# Test case: Check if RESOURCE_INTERVALS dictionary is properly structured
def test_resource_intervals():
    # Iterate through the RESOURCE_INTERVALS dictionary
    for resource, intervals in RESOURCE_INTERVALS.items():
        # Assert that each value is a list
        assert isinstance(intervals, list)
        # Assert that each list is not empty
        assert len(intervals) > 0
        # Assert that each interval is a string
        for interval in intervals:
            assert isinstance(interval, str)
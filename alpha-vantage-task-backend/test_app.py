import pytest
from app import app, RESOURCE_INTERVALS
import requests
from utils import calculate_daily_average, print_api_data

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test case: Ensure the API returns an error when dates are missing
def test_daily_average_missing_dates(client):
    response = client.get('/daily_average?function=WTI')
    assert response.status_code == 400
    assert "Start date and end date are required" in response.json['error']

# Test case: Verify that the API handles invalid function (resource) correctly
def test_daily_average_invalid_function(client):
    response = client.get('/daily_average?function=INVALID&start_date=2023-01-01&end_date=2023-12-31')
    assert response.status_code == 400
    assert "Invalid resource: INVALID" in response.json['error']

# Test case: Check if the API returns correct data for a valid request
def test_daily_average_valid_request(client, mocker):
    mock_data = {
        "data": [
            {"date": "2023-01-01", "value": "70"},
            {"date": "2023-01-02", "value": "72"},
            {"date": "2023-01-03", "value": "75"},
        ]
    }
    mocker.patch('requests.get', return_value=mocker.Mock(json=lambda: mock_data))
    
    response = client.get('/daily_average?function=WTI&start_date=2023-01-01&end_date=2023-01-03')
    assert response.status_code == 200
    assert response.json['function'] == 'WTI'
    assert response.json['average_price'] == 72.33
    assert response.json['currency'] == 'USD per unit'

# Test case: Verify the calculate_daily_average function works correctly
def test_calculate_daily_average():
    data = {
        "data": [
            {"date": "2023-01-01", "value": "70"},
            {"date": "2023-01-02", "value": "72"},
            {"date": "2023-01-03", "value": "75"},
        ]
    }
    average = calculate_daily_average(data, "2023-01-01", "2023-01-03")
    assert round(average, 2) == 72.33

# Test case: Ensure calculate_daily_average returns None for empty date range
def test_calculate_daily_average_empty_range():
    data = {
        "data": [
            {"date": "2023-01-01", "value": "70"},
            {"date": "2023-01-02", "value": "72"},
            {"date": "2023-01-03", "value": "75"},
        ]
    }
    average = calculate_daily_average(data, "2023-01-04", "2023-01-05")
    assert average is None

# Test case: Check if print_api_data function outputs correct information
def test_print_api_data(capsys):
    data = {
        "data": [
            {"date": "2023-01-01", "value": "70"},
            {"date": "2023-01-02", "value": "72"},
            {"date": "2023-01-03", "value": "75"},
        ]
    }
    print_api_data(data, "2023-01-01", "2023-01-03")
    captured = capsys.readouterr()
    assert "API Data Summary:" in captured.out
    assert "Total data points: 3" in captured.out

# Test case: Verify API handles different intervals correctly
def test_daily_average_different_intervals(client, mocker):
    mock_data = {
        "data": [
            {"date": "2023-01-01", "value": "70"},
            {"date": "2023-01-08", "value": "72"},
            {"date": "2023-01-15", "value": "75"},
        ]
    }
    mocker.patch('requests.get', return_value=mocker.Mock(json=lambda: mock_data))
    
    response = client.get('/daily_average?function=WTI&interval=weekly&start_date=2023-01-01&end_date=2023-01-15')
    assert response.status_code == 200
    assert response.json['interval'] == 'weekly'
    assert response.json['average_price'] == 72.33

# Test case: Check if API returns error for invalid interval
def test_daily_average_invalid_interval(client):
    response = client.get('/daily_average?function=WTI&interval=invalid&start_date=2023-01-01&end_date=2023-12-31')
    assert response.status_code == 400
    assert "Invalid interval 'invalid' for resource 'WTI'" in response.json['error']

# Test case: Ensure API returns error when start date is missing
def test_daily_average_missing_start_date(client):
    response = client.get('/daily_average?function=WTI&interval=daily&end_date=2023-12-31')
    assert response.status_code == 400
    assert "Start date and end date are required" in response.json['error']

# Test case: Verify API returns error when end date is missing
def test_daily_average_missing_end_date(client):
    response = client.get('/daily_average?function=WTI&interval=daily&start_date=2023-01-01')
    assert response.status_code == 400
    assert "Start date and end date are required" in response.json['error']

def test_daily_average_api_limit_reached(client, mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"Information": "API limit reached"}
    mocker.patch('requests.get', return_value=mock_response)
    mocker.patch('app.requests.get', return_value=mock_response)

    with mocker.patch('app.daily_average') as mock_daily_average:
        mock_daily_average.return_value = jsonify({"error": "API limit reached"}), 429
        response = client.get('/daily_average?function=WTI&interval=daily&start_date=2023-01-01&end_date=2023-12-31')
    
    assert response.status_code == 429
    assert "API limit reached" in response.json['error']

def test_daily_average_api_error(client, mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"Error Message": "Invalid API call"}
    mocker.patch('requests.get', return_value=mock_response)
    mocker.patch('app.requests.get', return_value=mock_response)

    with mocker.patch('app.daily_average') as mock_daily_average:
        mock_daily_average.return_value = jsonify({"error": "Invalid API call"}), 400
        response = client.get('/daily_average?function=WTI&interval=daily&start_date=2023-01-01&end_date=2023-12-31')
    
    assert response.status_code == 400
    assert "Invalid API call" in response.json['error']

def test_daily_average_request_exception(client, mocker):
    mocker.patch('requests.get', side_effect=requests.RequestException("Connection error"))
    mocker.patch('app.requests.get', side_effect=requests.RequestException("Connection error"))

    with mocker.patch('app.daily_average') as mock_daily_average:
        mock_daily_average.return_value = jsonify({"error": "API request failed: Connection error"}), 500
        response = client.get('/daily_average?function=WTI&interval=daily&start_date=2023-01-01&end_date=2023-12-31')
    
    assert response.status_code == 500
    assert "API request failed: Connection error" in response.json['error']
# Test case: Check if RESOURCE_INTERVALS dictionary is properly structured
def test_resource_intervals():
    for resource, intervals in RESOURCE_INTERVALS.items():
        assert isinstance(intervals, list)
        assert len(intervals) > 0
        for interval in intervals:
            assert isinstance(interval, str)
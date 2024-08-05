import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import './App.css';

const resourceIntervals = {
  WTI: ['daily', 'weekly', 'monthly'],
  BRENT: ['daily', 'weekly', 'monthly'],
  NATURAL_GAS: ['daily', 'weekly', 'monthly'],
  COPPER: ['monthly', 'quarterly', 'annual'],
  ALUMINUM: ['monthly', 'quarterly', 'annual'],
  WHEAT: ['monthly', 'quarterly', 'annual'],
  CORN: ['monthly', 'quarterly', 'annual'],
  COTTON: ['monthly', 'quarterly', 'annual'],
  SUGAR: ['monthly', 'quarterly', 'annual'],
  COFFEE: ['monthly', 'quarterly', 'annual'],
};

function App() {
  const [resource, setResource] = useState('WTI');
  const [interval, setInterval] = useState('daily');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    console.log('Resource changed to:', resource);
    console.log('Available intervals:', resourceIntervals[resource]);
    setInterval(resourceIntervals[resource][0]);
  }, [resource]);

  const handleResourceChange = (e) => {
    const newResource = e.target.value;
    setResource(newResource);
    console.log('Resource changed to:', newResource);
  };

  const fetchDailyAverage = async () => {
    setIsLoading(true);
    setError(null);
    setResult(null);
  
    if (!startDate || !endDate) {
      setError("Please select both start and end dates.");
      setIsLoading(false);
      return;
    }
  
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'https://alpha-vantage-task-backend.azurewebsites.net';      const url = `${backendUrl}/daily_average?function=${resource}&interval=${interval}&start_date=${startDate}&end_date=${endDate}`;
      console.log('Fetching from URL:', url);
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error('Fetch error:', err);
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const chartData = result
    ? [
        {
          name: `${result.function} (${result.interval})`,
          price: result.average_price,
        },
      ]
    : [];

  return (
    <div className="App">
      <h1>Commodity Average API</h1>
      <div>
        <label>
          Resource:
          <select
            value={resource}
            onChange={handleResourceChange}
          >
            <option value="WTI">Crude Oil (WTI)</option>
            <option value="BRENT">Crude Oil (Brent)</option>
            <option value="NATURAL_GAS">Natural Gas</option>
            <option value="COPPER">Copper</option>
            <option value="ALUMINUM">Aluminium</option>
            <option value="WHEAT">Wheat</option>
            <option value="CORN">Corn</option>
            <option value="COTTON">Cotton</option>
            <option value="SUGAR">Sugar</option>
            <option value="COFFEE">Coffee</option>
          </select>
        </label>
      </div>
      <div>
        <label>
          Interval:
          <select
            key={resource}
            value={interval}
            onChange={(e) => setInterval(e.target.value)}
          >
            {resourceIntervals[resource].map((int) => (
              <option key={int} value={int}>
                {int.charAt(0).toUpperCase() + int.slice(1)}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div>
        <label>
          Start Date:
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          End Date:
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </label>
      </div>
      <button onClick={fetchDailyAverage} disabled={isLoading}>
        {isLoading ? 'Loading...' : 'Fetch Data'}
      </button>
      {error && (
        <div className="error">
          <h3>Error:</h3>
          <p>{error}</p>
          {error.includes('API limit reached') && (
            <p>
              Consider upgrading your API plan or waiting before making more requests.
              You can find more information about API limits at{' '}
              <a href="https://www.alphavantage.co/premium/" target="_blank" rel="noopener noreferrer">
                Alpha Vantage Premium
              </a>
            </p>
          )}
        </div>
      )}
      {isLoading && <p className="loading">Loading data...</p>}
      {result && (
        <div className="result">
          <h2>Results:</h2>
          <p>Resource: {result.function}</p>
          <p>Interval: {result.interval}</p>
          <p>Start Date: {result.start_date}</p>
          <p>End Date: {result.end_date}</p>
          <p>Average Price: {result.average_price} {result.currency}</p>
        </div>
      )}
      {result && (
        <div className="chart">
          <h2>Price Visualization</h2>
          <BarChart width={600} height={300} data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="price" fill="#8884d8" />
          </BarChart>
        </div>
      )}
    </div>
  );
}

export default App;


/* test comment for github workflow test */
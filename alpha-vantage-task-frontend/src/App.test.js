import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';

// Mock the fetch function
global.fetch = jest.fn();

describe('App Component', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders the App component', () => {
    render(<App />);
    expect(screen.getByText('Daily Average API')).toBeInTheDocument();
  });

  test('renders input fields and button', () => {
    render(<App />);
    expect(screen.getByLabelText('Resource:')).toBeInTheDocument();
    expect(screen.getByLabelText('Interval:')).toBeInTheDocument();
    expect(screen.getByLabelText('Start Date:')).toBeInTheDocument();
    expect(screen.getByLabelText('End Date:')).toBeInTheDocument();
    expect(screen.getByText('Fetch Data')).toBeInTheDocument();
  });

  test('updates resource select value', () => {
    render(<App />);
    const resourceSelect = screen.getByLabelText('Resource:');
    fireEvent.change(resourceSelect, { target: { value: 'COPPER' } });
    expect(resourceSelect.value).toBe('COPPER');
  });

  test('updates interval select value', () => {
    render(<App />);
    const intervalSelect = screen.getByLabelText('Interval:');
    fireEvent.change(intervalSelect, { target: { value: 'weekly' } });
    expect(intervalSelect.value).toBe('weekly');
  });

  test('updates start date input value', () => {
    render(<App />);
    const startDateInput = screen.getByLabelText('Start Date:');
    fireEvent.change(startDateInput, { target: { value: '2023-01-01' } });
    expect(startDateInput.value).toBe('2023-01-01');
  });

  test('updates end date input value', () => {
    render(<App />);
    const endDateInput = screen.getByLabelText('End Date:');
    fireEvent.change(endDateInput, { target: { value: '2023-12-31' } });
    expect(endDateInput.value).toBe('2023-12-31');
  });

  test('fetches data and displays result', async () => {
    const mockResponse = {
      function: 'WTI',
      interval: 'daily',
      start_date: '2023-01-01',
      end_date: '2023-12-31',
      average_price: 75.50,
      currency: 'USD per barrel'
    };

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    render(<App />);
    
    fireEvent.click(screen.getByText('Fetch Data'));

    await screen.findByText('Results:');
    expect(screen.getByText('Resource: WTI')).toBeInTheDocument();
    expect(screen.getByText('Average Price: 75.50 USD per barrel')).toBeInTheDocument();
  });

  test('displays error message on API failure', async () => {
    fetch.mockRejectedValueOnce(new Error('API request failed'));

    render(<App />);
    
    fireEvent.click(screen.getByText('Fetch Data'));

    await waitFor(() => {
      expect(screen.getByText('Error: API request failed')).toBeInTheDocument();
    });
  });
});
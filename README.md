# Flight Price and Weather Data Scraper

This Python project fetches flight price data from Kayak and weather information from the OpenWeather API, then plots the data and saves it to a CSV file. The program uses web scraping with BeautifulSoup for flight prices and calls the OpenWeather API to gather weather information for a specific destination. It visualizes the data using Matplotlib and exports it to CSV for further analysis. You can use this program to collect data to see if prices fluctuate indirectly because of the weather due to tourism (Example: Salalah during the monsoon!)

## Prerequisites

Before running this project, ensure you have the following Python libraries installed:

- `requests`: For making HTTP requests to Kayak and OpenWeather APIs.
- `BeautifulSoup` (from `bs4`): For parsing the HTML content of Kayak to extract flight prices.
- `matplotlib`: For plotting flight prices and weather data.
- `python-dotenv`: For managing your environment variables (e.g., API keys).
- `csv`: Standard Python library for working with CSV files.

You can install the necessary packages by running:

```bash
pip install requests beautifulsoup4 matplotlib python-dotenv
```

## Project Structure

The project consists of several functions:
1. **`build_kayak_url`**: Constructs the Kayak URL for fetching flight prices based on the provided destination city, departure date, and return date.
2. **`scrape_flight_prices`**: Scrapes the flight prices from the Kayak page.
3. **`get_weather_data`**: Fetches the weather information from OpenWeather API for the provided city.
4. **`clean_weather_data`**: Cleans the raw weather data to extract relevant information (temperature, weather condition, etc.).
5. **`plot_prices_and_weather`**: Plots flight prices and corresponding weather data (temperature in Celsius) using Matplotlib.
6. **`save_to_csv`**: Saves the flight prices and weather data into a CSV file.

## How to Run

1. **Set up API Key**: Create a `.env` file in the project directory with the following content:
   ```
   api_key=YOUR_OPENWEATHER_API_KEY
   ```

   Replace `YOUR_OPENWEATHER_API_KEY` with your actual OpenWeather API key. You can obtain an API key by signing up at [OpenWeather](https://openweathermap.org/api).

2. **Run the Script**:
   You can run the script by executing the following command in your terminal:
   ```bash
   python script_name.py
   ```

   The script will prompt you to enter:
   - Destination city name (for weather data).
   - Destination airport code (for flight prices).
   - Departure date (in YYYY-MM-DD format).
   - Return date (in YYYY-MM-DD format).

3. **Output**:
   - The script will display a scatter plot of flight prices versus the weather at the destination.
   - It will also save the flight prices and weather data to a CSV file in the format `destination_city-departure_date.csv`.

## Example

- **Input**:
  ```
  Enter the destination city name for weather data: Tokyo
  Enter the destination airport code: TYO
  Enter the departure date (YYYY-MM-DD): 2024-10-25
  Enter the return date (YYYY-MM-DD): 2024-11-01
  ```

- **Output**:
  - A scatter plot of flight prices and the weather condition in Tokyo will be shown.
  - A CSV file `Tokyo-2024-10-25.csv` will be generated, containing the flight prices, weather information (temperature in Celsius), and weather condition.


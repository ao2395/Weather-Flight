import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from time import sleep

# Function to build Skyscanner URL based on city codes and dates
def build_skyscanner_url(departure_city_code, destination_city_code, departure_date, return_date):
    base_url = "https://www.skyscanner.com/transport/flights/nyc"
    url = f"{base_url}/{destination_city_code}/{departure_date}/{return_date}/?adultsv2=1&cabinclass=economy&childrenv2=&ref=home&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false"
    return url

# Function to scrape flight prices from Skyscanner
def scrape_flight_prices(url):
    response = requests.get(url)
    sleep(5)
    soup = BeautifulSoup(response.content, 'html.parser')
    prices = []

    # Attempt to find all span tags and filter by those containing dollar signs
    print(soup)
    span_tags = soup.find_all('span')
    for tag in span_tags:
        if '$' in tag.text:
            prices.append(tag.text.strip())

    if not prices:
        print("No prices found.")
    return prices


# Function to get weather data using OpenWeather API
def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get weather data for {city}")
        return None

# Function to clean the weather data
def clean_weather_data(raw_data):
    if raw_data:
        cleaned_data = {
            'City': raw_data.get('name', 'N/A'),
            'Temperature (K)': raw_data.get('main', {}).get('temp', 'N/A'),
            'Weather Condition': raw_data.get('weather', [{}])[0].get('description', 'N/A')
        }
    else:
        cleaned_data = {'City': 'N/A', 'Temperature (K)': 'N/A', 'Weather Condition': 'N/A'}
    return cleaned_data

# Function to plot flight prices and weather data
def plot_prices_and_weather(prices, weather_data):
    try:
        avg_prices = [float(price.replace('$', '').replace(',', '')) for price in prices]
        temp = float(weather_data.get('Temperature (K)', 273.15)) - 273.15  # Convert Kelvin to Celsius
        weather_condition = weather_data.get('Weather Condition', 'N/A')
    except ValueError:  # Handle non-numeric or missing values
        print("Error processing numerical data.")
        return
    
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Flight Number')
    ax1.set_ylabel('Price (USD)', color='tab:red')
    ax1.plot(range(len(avg_prices)), avg_prices, color='tab:red', label='Flight Prices')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    ax2 = ax1.twinx()  
    ax2.set_ylabel('Temperature (°C)', color='tab:blue')  
    ax2.axhline(temp, color='tab:blue', linestyle='--', label=f"Temperature ({weather_condition})")
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    plt.title(f"Flight Prices vs. Weather in {weather_data['City']}")
    fig.tight_layout()  
    plt.show()

# Example usage:
destination_city = input("Enter the destination city name for weather data: ").strip()
destination_airport_code = input("Enter the destination airport code: ").strip()
departure_date = input("Enter the departure date (YYMMDD): ")
return_date = input("Enter the return date (YYMMDD): ")
api_key = "b5fc77ee220b9988d70ea10665c8ab22"  # Replace with your OpenWeather API key

# Build Skyscanner URL
flight_url = build_skyscanner_url("nyc", destination_airport_code, departure_date, return_date)
print(f"Generated Skyscanner URL: {flight_url}")

# Scrape flight prices
flight_prices = scrape_flight_prices(flight_url)
print(f"Flight prices: {flight_prices}")

# Get weather data for destination
weather_data_raw = get_weather_data(destination_city, api_key)
cleaned_weather = clean_weather_data(weather_data_raw)
print(f"Weather data: {cleaned_weather}")

# Plot the flight prices and weather data
plot_prices_and_weather(flight_prices, cleaned_weather)

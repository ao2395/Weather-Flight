import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import csv 

load_dotenv()

# Access API key
api_key = os.getenv('api_key')
# mimic browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'

}
# Function to build kayak URL based on city codes and dates
def build_kayak_url(destination_city_code, departure_date, return_date):
    base_url = "https://www.kayak.com/flights/NYC-"
    url = f"{base_url}{destination_city_code}/{departure_date}/{return_date}?sort=bestflight_a"
    return url

# Function to scrape flight prices from Skyscanner
def scrape_flight_prices(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    prices = []
    # look for prices
    price_tags = soup.find_all('div', class_='f8F1-price-text')
    for tag in price_tags:
        price = tag.text.strip()
        if price.startswith('$'):
            prices.append(price)
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
    except ValueError:
        print("Error processing numerical data.")
        return
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Number Of Flights')
    ax1.set_ylabel('Price (USD)', color='tab:red')
    ax1.scatter(range(len(avg_prices)), avg_prices, color='tab:red', label='Flight Prices')
    ax2 = ax1.twinx()  
    ax2.set_ylabel('Temperature (°C)', color='tab:blue')  
    ax2.axhline(temp, color='tab:blue', linestyle='--', label=f"Temperature ({weather_condition})")
    plt.title(f"Flight Prices vs. Weather in {weather_data['City']}")
    fig.tight_layout()  
    plt.show()

# Function to save data to CSV
def save_to_csv(prices, weather_data, destination_city, departure_date):
    filename = f"{destination_city}-{departure_date}.csv"
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Price', 'City', 'Temperature (C)', 'Weather Condition'])
        for price in prices:
            writer.writerow([price, weather_data['City'], round(float(weather_data['Temperature (K)']) - 273.15, 2), weather_data['Weather Condition']])
    print(f"Data saved to {filename}")

# Main execution block
if __name__ == "__main__":
    destination_city = input("Enter the destination city name for weather data: ").strip()
    destination_airport_code = input("Enter the destination airport code: ").strip()
    departure_date = input("Enter the departure date (YYYY-MM-DD): ")
    return_date = input("Enter the return date (YYYY-MM-DD): ")

    # Build and fetch data
    flight_url = build_kayak_url(destination_airport_code, departure_date, return_date)
    flight_prices = scrape_flight_prices(flight_url)
    weather_data_raw = get_weather_data(destination_city, api_key)
    cleaned_weather = clean_weather_data(weather_data_raw)

    # Plot and save data
    plot_prices_and_weather(flight_prices, cleaned_weather)
    save_to_csv(flight_prices, cleaned_weather, destination_city, departure_date)

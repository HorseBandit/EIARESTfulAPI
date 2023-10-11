import requests
import json
import csv

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)

""" def fetch_data(api_key, year, month):
    base_url = "https://api.eia.gov/v2/electricity/retail-sales/data"
    
    params = {
        "api_key": api_key,
        "data[]": "price",
        "facets[stateid][]": "WA",
        "frequency": "daily",  # Set to hourly
        "sort[0][column]": "period",
        "sort[0][direction]": "asc"
    }
    
    results = []

    PAGE_SIZE = 1000

    start_date = f"{year}-{month:02}-01"
    if month == 12:
        end_date = f"{year+1}-01-01"
    else:
        end_date = f"{year}-{month+1:02}-01"

    params["start"] = start_date
    params["end"] = end_date
    offset = 0

    while True:  # Pagination loop
        params["length"] = PAGE_SIZE
        params["offset"] = offset

        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            current_data = data['response']['data']
            results.extend(current_data)

            # If returned data is less than PAGE_SIZE, end of data
            if len(current_data) < PAGE_SIZE:
                break

            offset += PAGE_SIZE  # Next "page" of data
        else:
            print(f"Failed to fetch data for {start_date}. Status Code: {response.status_code}")
            break

    return results """


def fetch_data(api_key, start_year, end_year):
    # Base API URL
    base_url = "https://api.eia.gov/v2/electricity/retail-sales/data"
    
    # Set the parameters based on the documentation provided
    params = {
        "api_key": api_key,
        "data[]": "price",
        "facets[stateid][]": "WA",   # For Washington
        "frequency": "monthly",      # For monthly data
        "sort[0][column]": "period",
        "sort[0][direction]": "asc", # For ascending order
    }
    
    # Create empty list to store the results
    results = []

    # Loop through the years
    for year in range(start_year, end_year+1):
        for month in range(1, 13):
            start_date = f"{year}-{month:02}-01"
            if month == 12:
                end_date = f"{year+1}-01-01"
            else:
                end_date = f"{year}-{month+1:02}-01"

            # Set the date range
            params["start"] = start_date
            params["end"] = end_date

            response = requests.get(base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()

                results.extend(data['response']['data'])

            else:
                print(f"Failed to fetch data for {start_date}. Status Code: {response.status_code}")

    return results

# Input your API key here
API_KEY = "KCD3egGfjWTPJN7seM8ttxRsjM2kh4yatC9otAAa"

data = fetch_data(API_KEY, 2019, 2023)

#fetched_data = data['response']['data']
save_to_csv(data, 'output.csv')




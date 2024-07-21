import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import json
from tqdm import tqdm
import matplotlib.pyplot as plt
from datetime import datetime

def get_user_agent_string(first_name : str, last_name : str, email : str) -> str:
    return f'{first_name} {last_name} ({email})'

def get_cik_ticker_map(user_agent_string : str) -> dict:

    headers = {
        'User-Agent': user_agent_string
    }

    # Download the CIK mapping file
    cik_map_url = "https://www.sec.gov/include/ticker.txt"
    response = requests.get(cik_map_url, headers=headers, timeout=10)

    if response.status_code == 200:
        # Store the CIK mapping in the Edgar class as a dictionary
        cik_map = {}
        for line in response.text.splitlines():
            ticker, cik = line.split('\t')
            # Pad the CIK with leading zeros to ensure it's 10 digits long
            padded_cik = cik.zfill(10)
            cik_map[ticker.lower()] = padded_cik
        print("CIK mapping downloaded successfully.")
        return cik_map
    else:
        print(f"Failed to download CIK mapping. Status code: {response.status_code}")
        return 
        
def get_cik_from_ticker(ticker : str, cik_map : dict) -> str:
    ticker = ticker.lower()
    return cik_map[ticker]

def get_dict(path : str):
    with open(path, 'r') as file:
        my_dict = json.load(file)
    return my_dict

def save_dict(my_dict : dict, path : str):
    with open(path, 'w') as file:
        json.dump(my_dict, file)


def get_data_by_tag(user_agent_string : str, cik : str, tag : str, taxonomy : str = "us-gaap") -> dict:
    headers = {
        'User-Agent': user_agent_string
    }
    url = f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/{taxonomy}/{tag}.json'
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

def get_company_data(
    user_agent_string : str,
    cik : str,
    tags_dict : str,
    taxonomy : str = "us-gaap"
    ):

    historical_data = {}

    for key in tqdm(tags_dict.keys(), desc="Getting data by tag"):

        data = get_data_by_tag(
            user_agent_string,
            cik,
            key,
        )

        historical_data[key] = data
    
    return historical_data

def get_data_by_tag(data_obj : dict, tag : str):
    data = []
    for item in data_obj[tag]['units']['USD']:
        data.append((item['end'], item['val']))
    return data

def plot(data : list[tuple[str, float]], title : str, path : str):

    dates = [datetime.strptime(date, '%Y-%m-%d') for date, _ in data]
    values = [value for _, value in data]
    
    # Extract dates and values from the data
    dates = [datetime.strptime(date, '%Y-%m-%d') for date, _ in hi]
    values = [value for _, value in hi]

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(dates, values, marker='o')

    # Customize the plot
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.grid(True)

    # Rotate and align the tick labels so they look better
    plt.gcf().autofmt_xdate()

    # Use a tight layout to prevent the x-label from being cut off
    plt.tight_layout()

    # Display the plot
    plt.savefig(path)
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np


# Gets the titles of the movies for which we have scripts
ready_scripts = [file_name[:file_name.find("_")] for file_name
                 in os.listdir(os.getcwd() + "/scripts/")
                 if ".txt" in file_name]

# Will store the data for each title
org_title, prep_title = [], []
release_date, prod_budget, dom_gross, world_gross = [], [], [], []
website_url = requests.get("https://www.the-numbers.com/movie/budgets/all").text


def get_data():

    """ Scrapes the data from https://www.the-numbers.com/movie/budgets/all """
    soup = BeautifulSoup(website_url, "lxml")
    movies = soup.find_all("tr")[1:]
    for movie in movies:
        original_title = movie.find("b").string
        # Gets the title that will match the titles we have saved as movie scripts
        processed_title = original_title.replace(": ", "-").replace(" ", "-").replace("â\x80\x99", "\'")
        if processed_title[:4] == "The-":
            processed_title = processed_title[processed_title.find("The-")+4:] + "," + "-The"
        # If the script is in our directory, gets the data
        if processed_title in ready_scripts and processed_title not in prep_title:  # Avoids duplicates
            org_title.append(original_title.replace("â\x80\x99", "\'"))
            prep_title.append(processed_title)
            release_date.append(movie.find("a").string)
            numbers = movie.find_all("td", {"class": "data"})
            prod_budget.append(int(numbers[1].string[1:].replace(",", "")))
            dom_gross.append(int(numbers[2].string[1:].replace(",", "")))
            world_gross.append(int(numbers[3].string[1:].replace(",", "")))


get_data()
# Does the same for all the web pages 
for i in range(101, 5800, 100):
    website_url = requests.get("https://www.the-numbers.com/movie/budgets/all/" + str(i)).text
    get_data()

# Creates DataFrame 
df = pd.DataFrame({"Processed Title": prep_title, "Release Date": release_date,
                   "Production Budget ($)": prod_budget, "Domestic Gross ($)": dom_gross,
                   "Worldwide Gross ($)": world_gross}, index=org_title)
# Replaces 0s with np.Nans and drops them
df.replace(0, np.NaN, inplace=True)
df.dropna(inplace=True)
# Gets ROI columns
df["Domestic ROI (%)"] = (df["Domestic Gross ($)"] - df["Production Budget ($)"])*100/df["Production Budget ($)"]
df["Worldwide ROI (%)"] = (df["Worldwide Gross ($)"] - df["Production Budget ($)"])*100/df["Production Budget ($)"]
# Saves the data as csv 
df.to_csv("success_data.csv")


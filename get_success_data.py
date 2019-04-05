import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import numpy as np
import operator

def get_characters(script, threshold_char=5, threshold_space=-1):
    """ Gets the characters of a script """
    with open(os.getcwd() + "/scripts/" + script, "r") as s:
        script = s.read()
        
    poss_char = {}
    for line in script.split("\n"):
        if line.count(" ") > threshold_space:
            key = line.strip(" ").replace(line[line.find("("):line.find(")") + 1], "").strip(" ").replace("\t", "").strip(" ")
            if key not in poss_char:
                poss_char[key] = 1
            else:
                poss_char[key] += 1
                        
    sorted_poss_chars = sorted(poss_char.items(), key=operator.itemgetter(1), reverse=True)
    chars = []
    for char_tuple in sorted_poss_chars:
        if char_tuple[1] > threshold_char:
            chars.append(char_tuple)
        else:
            break
            
    return [char[0] for char in chars if char[0] != "" and "-" not in char[0] and "." not in char[0] and ":" not in char[0] and "?" not in char[0]]

# Gets the titles of the movies for which we have scripts
ready_scripts = [file_name[:file_name.find("_")] for file_name
                 in os.listdir(os.getcwd() + "/scripts/")
                 if ".txt" in file_name]
n_scripts_before = len(ready_scripts)

for script in ready_scripts:
    path = os.getcwd() + "/scripts/" + script + "_script.txt"
    with open(path, "r") as s:
        m = s.read()
    # Deletes scripts that were pdf and thus we got html trash
    if len(m) < 3000:
        os.remove(path)
        continue
    # Deletes scripts that do not follow the standard format
    # Such us: MULAN: Hey yo what's up?
    # Instead of:         MULAN
     #              Hey yo what's up?
    if len(get_characters(script + "_script.txt")) == 0:
        os.remove(path)
        
ready_scripts = [file_name[:file_name.find("_")] for file_name
                 in os.listdir(os.getcwd() + "/scripts/")
                 if ".txt" in file_name]
print("We removed", n_scripts_before - len(ready_scripts), "scripts")  # We removed 23 scripts
print("There are", len(ready_scripts), "scripts now")

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


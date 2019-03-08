import requests
from bs4 import BeautifulSoup
import os
from time import time


def scrape_script(movie_title, print_error=False):
    """
    Scrapes a movie script from https://www.imsdb.com and saves it
    as "movie_title.txt" in the "scripts" subdirectory

    :param movie_title: each word needs to be joined by a "-"
    for example: "Guardians-of-the-Galaxy-Vol-2"
    Note that some of the titles will require special spelling
    so it is always best to check on https://www.imsdb.com
    :param print_error: if True, prints out a warning when the request fails 
    or when there is no text under the script tag
    """
    # Catches any exception raised by either the request, the parsing
    # or when looking for the tag that contains the script
    try:
        website_url = requests.get("https://www.imsdb.com/scripts/" + movie_title + ".html").text
        soup = BeautifulSoup(website_url, "html.parser")
        script = str(soup.pre)
    except Exception as e:
        if print_error:
            print(e)
            print(movie_title + ": Either the script is not available or you entered a wrong title")
    else:
        # Checks if we got some real text inside this tag (it can be the case that an exception is not
        # raised but there is also not a script in the url)
        if len(script) < 1000:
            if print_error:
                print(movie_title + ": Either the script is not available or you typed the title wrong")
        else:
            # Gets rid of initial tag and bold tag
            script = script.replace("<pre>", "").replace("</pre>", "")
            script = script.replace("<b>", "").replace("</b>", "")
            # Saves the script into a .txt file
            if "/" in movie_title:  # Annoying "/" :/ 
                pass
            else:
                with open(os.getcwd() + "/scripts/" + movie_title + "_script.txt", "w") as s:
                    s.write(script)


# Let's try it with a few movies
# movie_titles = ["Coco", "Guardians-of-the-Galaxy-Vol-2", "Avatar", "Birdman", "Batman-Begins"]
# for title in movie_titles:
#     scrape_script(title, print_error=True)

# Gets movie titles from the link below (TODO: get ROI, probably % is better)
website_url = requests.get("https://www.the-numbers.com/movie/budgets/all").text
soup = BeautifulSoup(website_url, "lxml")
titles = [tag.string.replace(" ", "-").replace("â\x80\x99", "\'") for tag in soup.table.find_all("b")]
for i in range(101, 5800, 100):
    website_url = requests.get("https://www.the-numbers.com/movie/budgets/all/" + str(i)).text
    soup = BeautifulSoup(website_url, "lxml")
    titles += [tag.string.replace(" ", "-").replace("â\x80\x99", "\'") for tag in soup.table.find_all("b")]

# Tries to get the scripts for all the movie titles (most will fail)
start = time()
for title in titles:
    scrape_script(title)
end = time() - start
print("The scraping process took", round(end), "seconds")  # The scraping process took 2257 seconds

# Gets the titles whose scripts we actually managed to get
ready_scripts = [file_name[:file_name.find("_")] for file_name
                 in os.listdir(os.getcwd() + "/scripts/")
                 if ".txt" in file_name]
print("Out of", len(titles), "movies,", "we only got", len(ready_scripts), "scripts")  # Out of 5702 movies we only got 538 scripts





import requests
from bs4 import BeautifulSoup


def scrape_script(movie_title):
    """
    Scrapes a movie script from https://www.imsdb.com and saves it
    as "movie_title.txt" in the same directory this script is located

    :param movie_title: each word needs to be joined by a "-"
    for example: "Guardians-of-the-Galaxy-Vol-2"
    Note that some of the titles will require special spelling
    so it is always best to check on https://www.imsdb.com
    """
    # Catches any exception raised by either the request, the parsing
    # or when looking for the tag that contains the script
    try:
        website_url = requests.get("https://www.imsdb.com/scripts/" + movie_title + ".html").text
        soup = BeautifulSoup(website_url, "html.parser")
        script = str(soup.pre)
    except Exception as e:
        print(e)
        print(movie_title + ": Either the script is not available or you entered a wrong title")
    else:
        # Checks if we got some real text inside this tag (it can be the case that an exception is not
        # raised but there is also not a script in the url)
        if len(script) < 1000:
            print(movie_title + ": Either the script is not available or you typed the title wrong")
        else:
            # Gets rid of initial tag and bold tag
            script = script.replace("<pre>", "").replace("</pre>", "")
            script = script.replace("<b>", "").replace("</b>", "")
            # Saves the script into a .txt file
            with open(movie_title + "_script.txt", "w") as s:
                s.write(script)


# Let's try it with a few movies
movie_titles = ["Coco", "Guardians-of-the-Galaxy-Vol-2", "Avatar", "Birdman", "Batman-Begins"]
for title in movie_titles:
    scrape_script(title)


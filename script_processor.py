import os
import requests
from bs4 import BeautifulSoup
import omdb
import json

files = os.listdir('NLP-Movie_Scripts/scripts/')

#Create a a dict where each item contains information on a movie in dictionary format
movies = {}
for each in files:
    movie = {}
    if '-The_script.txt' in each:
        movies['The '+each.replace('-The_script.txt','').replace('-', ' ')[:-1]] = {'filename':each}
    else:
        movies[each.replace('_script.txt','').replace('-', ' ')] = {'filename':each}

#fetch imdb data of a movie using OMDB api, please read OMDB doc for further details
def getOmdbData(movie):
    api_key = 'eb6547ff'
    omdb.set_default('apikey', api_key)
    return omdb.get(title=movie, fullplot=True, tomatoes=True)

def prepURL(imdb_id):
	#prepare the url from which we will scrape the cast data
    url = 'https://www.imdb.com/title/'+imdb_id #+'/fullcredits?ref_=tt_cl_sm#cast'
    return url

def getCharacters(url):
	#Only first imdb page of the cast members are considered. 
    website_url = requests.get(url).text
    soup = BeautifulSoup(website_url, "lxml")
    #upon inspecting the html code, we see that the cast is structured in <table> tags
    table = soup.find('table',{'class':'cast_list'}) 
    #<tr> is a tag for table row [tr]
    cast = table.find_all('tr') 
    characters = []
    for each in cast:
        temp = each.find_all('td')[-1].text.strip().replace('\n','').replace('  ','')
        if 'uncredited' in temp:
            characters.append(temp.split('(')[0][:-1])
        else:
            characters.append(temp)
    characters = list(set(characters))
    return characters

for movie in movies.keys():
	#for the given movie name we fetch the imdb data
    x = getOmdbData(movie)
    try:
        movies[movie]['imdb_id'] = x['imdb_id']
    except:
        continue

#We need to delete the movie's on which there isn't much data available
delete = []
for movie in movies.keys():
    try:
        url = prepURL(movies[movie]['imdb_id'])
        characters = getCharacters(url)
        movies[movie]['imdb_url'] = url
        movies[movie]['characters'] = characters
    except:
        delete.append(movie)

#Delete the movies on which we don't have necessary data on
for movie in delete:
    del movies[movie]

#Clean the data further
for movie in movies.keys():
    if 'Cast overview, first billed only:' in movies[movie]['characters']:
        movies[movie]['characters'].remove('Cast overview, first billed only:')

#Alternate Approach which works equally well.
"""
script = open('NLP-Movie_Scripts/scripts/'+file,'r')
for line in script:
    temp = line.strip()
    if 'thor'.upper() in temp:
        if (len(temp.split(' '))  <= 2) & (temp.split(' ')[0]=='thor'.upper()):
            print(temp)
"""
for movie in movies.keys():
    script = open('NLP-Movie_Scripts/scripts/'+movies[movie]['filename'],'r').read()
    #create a string containing character names seperated by commas
    characters = ','.join([','.join(name.split(' ')) for name in movies[movie]['characters'] if len(name.split(' ')) <3])
    # data structure to store the dialogues
    dialogues = {}
    for ch in characters.split(','):
        if 'Mr.' in ch or '-' in ch:
            continue
        else:
            name = ch
        dialogue = '' 
        flag = 0
        count = 0
        for line in script.split("\n"):
            temp = line.strip(" ").replace(line[line.find("("):line.find(")") + 1], "").strip(" ")
            if temp.isupper():  # If Character Intro
                if  name.upper() in temp:
                    flag = 1
                    count += 1
                    dialogue += '\n['+str(count)+']'
                    continue
                else:  # If it's another character
                    flag = 0
                    continue
            if flag:
                if flag == 1:
                    ident_level_first = len(line) - len(line.lstrip(" "))
                ident_level = len(line) - len(line.lstrip(" "))
                if ident_level == ident_level_first:
                    dialogue += temp + " "
                else:
                    continue
                flag += 1
        dialogues[name] = dialogue
    movies[movie]['dialogues'] = dialogues


#information available on each movie ---- dict_keys(['filename', 'imdb_id', 'imdb_url', 'characters', 'dialogues'])
for movie in movies.keys():
    with open(movie.replace(' ','_')+'.json', 'w') as fp:
        json.dump(movies[movie], fp)
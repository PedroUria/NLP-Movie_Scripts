# Write any features that will be extracted per character in this script
# NOTE: The code used for the already extracted is commented out
# You should do the same once you extract the feature and save it on the csv

import pandas as pd
import os
import json
import operator
import nltk
from nltk.tokenize import word_tokenize
#from nltk.stem.porter import *
#porter_stemmer = PorterStemmer()
#from readability import Readability  # https://github.com/cdimascio/py-readability-metrics
#stop_words = nltk.corpus.stopwords.words('english')
#from profanity_check import predict  # https://github.com/vzhou842/profanity-check


main_dict_path = os.getcwd()[:os.getcwd().find("feat_extraction")]
#movies = pd.read_csv(main_dict_path + "success_data.csv", index_col=0)
#movies["Success"] = movies.apply(lambda row: 1 if row["Worldwide ROI (%)"] > 0 else 0, axis=1)
#movies.drop(movies.columns[1:7], axis=1, inplace=True)

movies = pd.read_csv("movies_with_feats.csv", index_col=0)

path = main_dict_path + "diag_jsons/"
#n_unique_words_dict = {"n_unique_words_char_1": [], "n_unique_words_char_2": [],
#                      "n_unique_words_char_3": [], "n_unique_words_char_4": [],
#                      "n_unique_words_char_5": []}
#read_level_dict = {"FK_read_level_char_1": [], "FK_read_level_char_2": [],
#                   "FK_read_level_char_3": [], "FK_read_level_char_4": [],
#                   "FK_read_level_char_5": []}
#n_stop_words = {"n_stop_words_char_1": [], "n_stop_words_char_2": [],
#               "n_stop_words_char_3": [], "n_stop_words_char_4": [],
#               "n_stop_words_char_5": []}
#n_curse_words = {"n_curse_words_char_1": [], "n_curse_words_char_2": [],
#               "n_curse_words_char_3": [], "n_curse_words_char_4": [],
#               "n_curse_words_char_5": []}

############################################
# INCLUDE DICTS TO STORE MORE FEATURES BELOW
############################################

for script in movies["Processed Title"]:
    
    with open(path + script + "_script.json") as s:
        char_diags = json.loads(s.read())
        
    # Gets the dictionary for only the 5 characters with the most dialogue
    dict_lengths = {}
    for key, value in char_diags["dialogues"].items():
        a = value.replace("\n", "").replace(" ", "")
        i = 1
        while True:
            before = len(a)
            a = a.replace("[" + str(i) + "]", "")
            i += 1
            if len(a) == before:
                break
        dict_lengths[key] = len(a)
    top_chars = [char[0] for char in sorted(dict_lengths.items(), key=operator.itemgetter(1), reverse=True)[:5]]
    all_chars = list(char_diags["dialogues"].keys())
    for char in all_chars:
        if char not in top_chars:
            del char_diags["dialogues"][char]
    
    # Loops over the characters dialogues to extract some features (per character)
    n_char = 1
    for dialogue in char_diags["dialogues"].values():
        # Gets the dialogue in one long sentence and without [i]
        diag = dialogue.replace("\n", "")
        i = 1
        while True:
            before = len(diag)
            diag = diag.replace("[" + str(i) + "]", "")
            i += 1
            if len(diag) == before:
                break
        # Gets list of words per character
        words = word_tokenize(diag)
        
        # FEAT #1: # Number of Unique words per character --> Numerical
        # Stems the tokens
        #punct_sings = ".!?,;:-_--\'\'\'``..."
        #words_stemmed = [porter_stemmer.stem(word) for word in words if word not in punct_sings]
        # Gets the number of unique stems
        #n_unique_words_dict["n_unique_words_char_" + str(n_char)].append(len(set(words_stemmed)))
        
        # FEAT #2: Flesch Kincaid Read Level per character --> Categorical
        # https://github.com/cdimascio/py-readability-metrics
        #r = Readability(diag)
        #read_level_dict["FK_read_level_char_" + str(n_char)].append(r.flesch_kincaid().grade_level)
        #prob.append(script)
        
        # FEAT #3: Number of Stop Words per character --> Numerical
        #n_stop_words["n_stop_words_char_" + str(n_char)].append(len(set([w for w in words if w.lower() in stop_words])))
        
        # FEAT #4: Number of curse words per character -> Numerical
        # https://github.com/vzhou842/profanity-check
        #n_curse = 0
        #for word in words:
        #    if predict([word]): 
        #        n_curse += 1
        #n_curse_words["n_curse_words_char_" + str(n_char)].append(n_curse)
        #print(script, "character_" + str(n_char), "done\n")

        #######################################################
        # INCLUDE CODE TO EXTRACT MORE FEATURES BELOW
        #######################################################
        
        n_char += 1


def append_feature(feature_dict):
    for key in feature_dict.keys():
        movies[key] = feature_dict[key]


#append_feature(n_unique_words_dict)
#append_feature(read_level_dict)
#append_feature(n_stop_words)
#append_feature(n_curse_words)

#############################################
# INCLUDE append_feature(new_feat_dict) BELOW
#############################################

movies.to_csv("movies_with_feats.csv")


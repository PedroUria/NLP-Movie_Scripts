import os
import json
import operator


def get_characters(script, threshold_char=5, threshold_space=-1):
    
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
            
    return [char[0] for char in chars if char[0] != "" and "-" not in char[0] and "." not in char[0] and ":" not in char[0] and "?" not in char[0] and len(char[0]) > 1]


#Alternate Approach which works equally well.
"""
script = open('NLP-Movie_Scripts/scripts/'+file,'r')
for line in script:
    temp = line.strip()
    if 'thor'.upper() in temp:
        if (len(temp.split(' '))  <= 2) & (temp.split(' ')[0]=='thor'.upper()):
            print(temp)
"""
movies_diag = {}
for movie in os.listdir(os.getcwd() + "/scripts/"):
    movies_diag[movie] = {}
    if movie[-4:] == ".txt":
        with open(os.getcwd() + "/scripts/" + movie, "r") as s:
            script = s.read()
        #create a string containing character names seperated by commas
        characters = ','.join([name for name in get_characters(movie) if len(name.split(' ')) < 5])
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
                temp = line.strip(" ").replace(line[line.find("("):line.find(")") + 1], "").strip(" ").replace("\t", "").strip(" ")
                if temp.isupper():  # If Character Intro
                    if name.upper() == temp:
                        flag = 1
                        count += 1
                        dialogue += '\n['+str(count)+']'
                        continue
                    else:  # If it's another character
                        flag = 0
                        continue
                if flag:
                    if flag == 1:
                        if line.strip(): # Accounts for first lines == "" or == "     "
                            if line.lstrip("\t").lstrip(" ")[0] == "(" or line.rstrip(" ")[-1] == ")":  # To still get the dialogue
                                ident_level_first = None  # when the first line below a character
                                flag = 0  # intro is something like "(looking around with a grin)"
                            else:  # which describes how the character is acting but it is not his dialogue
                                if "\t" in line:  # To account for format where there are "\t" instead of "   "
                                    ident_level_first = line.count("\t")
                                else:
                                    ident_level_first = len(line) - len(line.lstrip(" "))
                        else:
                            ident_level_first = None
                            flag = 0
                    if "\t" in line:
                        ident_level = line.count("\t")
                    else:
                        ident_level = len(line) - len(line.lstrip(" "))
                    if ident_level_first:
                        if ident_level == ident_level_first:
                            dialogue += temp + " "
                        else:
                            continue
                    else:
                        pass
                    flag += 1
            dialogues[name] = dialogue
        movies_diag[movie]['dialogues'] = dialogues

#information available on each movie ---- dict_keys(["dialogues"])
for movie in movies_diag.keys():
    with open(os.getcwd() + "/diag_jsons/" + movie.replace('.txt','.json'), 'w') as fp:
        json.dump(movies_diag[movie], fp)


# Deletes scripts with weird formats 
# Spotted after inspection by doing
#a = []
#for i in os.listdir(os.getcwd() + "/diag_jsons/"):
#    with open(os.getcwd() + "/diag_jsons/" + i, "r") as s:
#        if len(s.read()) < 2000:
#            a.append(i)
#os.remove(os.getcwd() + "/scripts/" + "Road,-The_script.txt")
#os.remove(os.getcwd() + "/scripts/" + "True-Grit_script.txt")
#os.remove(os.getcwd() + "/scripts/" + "Armageddon_script.txt")
#os.remove(os.getcwd() + "/diag_jsons/" + "Road,-The_script.json")
#os.remove(os.getcwd() + "/diag_jsons/" + "True-Grit_script.json")
#os.remove(os.getcwd() + "/diag_jsons/" + "Armageddon_script.json")
# Deletes more problematic scripts... spotted 
# when doing Flesch-Kincaid Grade Level
#probs = ['9', 'Alien-Resurrection', 'American-History-X', 'American-Psycho', 'Big', 
#'Dogma', 'Ex-Machina', 'Finding-Nemo', 'Gangs-of-New-York', 'Ghostbusters', 'Gravity',
#'Heavenly-Creatures', 'Kids', 'Lock,-Stock-and-Two-Smoking-Barrels', 'Office-Space', 'Titanic']
#for script in probs:
#    os.remove(os.getcwd() + "/scripts/" + script + "_script.txt")
#    os.remove(os.getcwd() + "/diag_jsons/" + script + "_script.json")


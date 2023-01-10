# Instructions:
'''To run this the spell checker on a file with a specific dictionary, call the main function with the first parameter as the name
of the .txt file you want to spell check and the second parameter as the name of the dictionary you want to run it with'''

'''To create a new dictionary from a .txt file, call the SpecificDictionary method with two arguments, the .txt file you want to
use to maek a dictionary and the name you want to give to the dictionary'''

'''The improvement 2 method lets you structure your dictionary regardless of whether or no it was made into an unordered set.'''

import time
import os

begin = time.time()

def edit_DP(S,T):

    n = len(S)
    m = len(T)

    dp = [[0 for x in range(m + 1)] for x in range(n + 1)]
    

    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0:
                dp[i][j] = j

            elif j == 0:
                dp[i][j] = i

            elif S[i-1] == T[j-1]:
                dp[i][j] = dp[i-1][j-1]

            else:
                dp[i][j] = 1 + min(dp[i][j-1], #insert
                                    dp[i-1][j],  #delete
                                    dp[i-1][j-1])   #replace
    return dp[n][m]

str1 = "analysis"
str2 = "algorithms"
print(edit_DP(str1, str2))

#print(f"Total runtime of the program is {end - begin}")



def edit_distance_recursive(S,T):
 
    #Base case:
    #if S is empty, return the length of T
    if S == "":
        return len(T)
   
    #Base case:
    #if T is empty, return the length of S
    if T == "":
        return len(S)
 
    #Recursive case:
    #if the last characters of the two strings are the same, ignore last character and get the count for the remaining string
    elif S[:-1] == T[:-1]:
        return edit_distance_recursive(S[:-2],T[:-2])
 
    #Recursive case:
    #if the last characters are not same, consider three operations(insert, delete, replace) on the last character of first string
    #and recursively compute the minimum cost of all three operations and return the minimum of the three values
    else:
        return 1 + min(edit_distance_recursive(S[0:len(S)],T[:-1]), #insert
                        edit_distance_recursive(S[:-1],T[0:len(T)]), #delete
                        edit_distance_recursive(S[:-1], T[:-1])) #replace


def SpellChecker(strToCheck, dictionaryFile):
    # Opening the dictionary text file to read from
    with open(dictionaryFile + ".txt") as file:
        lines = list(line for line in (l.strip() for l in file) if line)

    # Creating a temp variable to store strToCheck without punctuations
    temp = ""
    punc = " -'’abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" 

    # Removing punctuations from strToCheck
    for character in strToCheck:
        if character in punc:
            temp += character


    temp.strip()
    
    # Creating two word lists that are lower case and split by whitespace characters
    wordList = temp.lower().split(" ")
    newWordList = temp.lower().split(" ")

    # Outputting the word list to see the line the spell checker will be checking
    print(newWordList)

    # Removing words that are correct according to the dictionary
    for word in wordList:
        if word in lines:
            newWordList.remove(word)

    # Removing empty characters (created by stripping out numbers etc.)
    for word in wordList:
        if word == '':
            newWordList.remove(word)
    
    # A list that holds 5 corrections to return to the user
    correctionsList = []

    # Adding each word of particular edit distance to a dictionary with keys = edit distance and values =
    # a list of words of that edit distance
    for word in newWordList:
        ED ={}
        for line in lines:
            if edit_DP(word, line[0:-1]) not in ED: # 0 to -1 split removes newline characters
            
                ED[edit_DP(word, line[0:-1])] = list()
            else:
                (ED [edit_DP(word, line[0:-1])].append(line))
        # formatting the output
        corrections = ["Mispelled Word: " + word + " Corrections:"]
        for key in sorted(ED.keys()):
            for item in ED[key]:
                corrections.append(item)
        # Appending the first 4 corrections to our return variable
        correctionsList.append(corrections[0:6])

    return print(correctionsList)

# main function of sorts, calls spellchecker, reads a file to check and formatss the output
# includes a stopwatch to time the time taken to find the corrections
def main(filename, dictName):
    # openning the file to be checked and reading it
    with open(filename + ".txt") as file:
        lines = list(line for line in (l.strip() for l in file) if line)
    # stopwatch
    begin = time.time()
    #formatting the output for every line in the file to be checked
    for line in lines:
        tempVar = SpellChecker(line, dictName)
        end = time.time()
        print("Corrections: ")
        print(tempVar)
        print(str(end - begin))
        print(" ")
            

# This method was used to create a domain specific dictionary of CS375
def SpecificDictionary(filename, dictName):
    # opening a file to read
    with open(filename + ".txt") as file:
        lines = file.readlines()
    
    # a string of punctuations
    punc = "\'’abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"     

    # two lists that will contain words
    wordList = []
    newList = []

    # appending all the words (along with punctuation) to word list, splitting at the whitespace
    for line in lines:
        split = line.split(" ")
        for item in split:
            wordList.append(item)

    #lines = set(lines)
    # removing the punctuation from each word in the word list
    for word in wordList:
        word = word.strip()
        eme = ""
        for i in range(len(word)):
            if word[i] in punc:
                eme += word[i]
            else:
                eme += "\n"
        newList.append(eme)

    # writing the words from the newlist to the dictionary
    with open(dictName + '.txt', 'w') as fileWrite:
        for word in newList:
            word = word.lower()
            word = word.strip()
            if word != "\n" and word != "":
                fileWrite.write(word + "\n")
    # removing all duplicates from the dictionary
    SetMaker(dictName, dictName)
    
# Helper function to help make the dictionary without repeats
def SetMaker(filename, dictName):
    with open(filename + ".txt") as file:
        lines = file.readlines()

    lines = set(lines)

    with open(dictName +'_', 'w') as fileWrite:
        for line in lines:
            fileWrite.write(line)
    os.remove(dictName + ".txt")
   

# Code that created our dictionary for improvement 2
def Improvement2():
    # Opens a txt file with the top 10000 words on google
    with open('top10000' + ".txt") as file:
        lines = file.readlines()
    # Opens the dictionary we were originally working with
    with open('dictionary' + ".txt") as file:
        words = file.readlines()
    # Creates a new txt file to put our modified dictionary in
    with open('Improvement3.txt', 'w') as fileWrite:
        for line in lines:
                fileWrite.write(line)
        # Loop that makes sure the words in the top 10000 words 
        # aren't repeated anywhere
        for word in words:
            if word not in lines:
                fileWrite.write(word + "\n")


#importing required modules
from types import WrapperDescriptorType
from numpy import character, negative
import pandas as pd
import requests
import os,string
import openpyxl
from bs4 import BeautifulSoup as bs
from nltk.tokenize import word_tokenize
from textstat.textstat import textstatistics,legacy_round
import re
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
}

#Extracting the data

def extract_data(filename):                                         #takes Input filename as parameter which contains urls for articles
    urls = pd.read_excel(filename,index_col=0)                      #read excel file as dataframe
    for i in urls.index:                                            #loop over urls.index
        r = requests.get(urls['URL'][i],headers=headers)            #sends a request to respective webpage
        htmlcontent = r.content                                     #extract content from webpage
        soup = bs(htmlcontent,'html.parser')                        # parse content using beautifulsoup
        #Extract all the paragraphs
        paras = soup.find_all('p')                                   #finds all the paragraph in a webpage
        text = ""
        for para in paras:
            text = text +para.get_text()    

        title = soup.find('title').get_text()                        #extract the title ftom webpage

        with open(f"{i}.txt",'w',encoding = 'utf-8') as f:           #create a text file with name as url_id.txt
            f.write(f'{title}')                                      # write title in the text file
            f.write(f'{text}')                                       # write article paragraphs in the text file



# analysing data 

# 1. cleaning the data 
    # Function to covnvert the text into lowercase
def lower_txt(file):                                                 #takes text file name as a input 
    lower_txt= ""                                            
    with open(file,"r",encoding="utf-8") as f:                       #open the file in read mode 
        for line in f:                                               #loop over lines in a text file 
            lower_txt = lower_txt + line.lower()                     #convert lines into lowercase and add them to a string named lower_text
        return lower_txt                                             #returns lower_text
  
    #Remove Punctuation 

def rem_punct(file):                                                 #takes text file name as a input 
    raw_text = lower_txt(file)                                       #lowers the text using lower_text() function
    for element in raw_text:                                         #loops over every character of a string
        if element in string.punctuation:                            #checks if character matches with any punctuation
            raw_text = raw_text.replace(element, "")                 #if character matches with any punctuation then it removes it
    return raw_text                                                  #returning text with removed punctuation


    #Remove Stopwords

def remove_stop_words(file,stopwords):                               #Takes two parameters textfile name and stopwords file name
    rem_punct_text = rem_punct(file)                                 #our first step is two remove punctuations
    stopwords_text = []                                              #A list to store stopwords
    with open(stopwords,'r',encoding="utf-8") as f:                  #open stopword file in read mode
        for line in f.readlines():                                   #read everyline to get stopwords
            stopwords_text.append(line)                              #appends stopwords list by adding stopwords
    rem_punct_list = [x for x in rem_punct_text.split()]             #list of words with remove punctuations
    clean_txt =  [word for word in rem_punct_list if word not in stopwords_text]  #remove stopwords from textfile
    return clean_txt                                                               #Returns Clean text
    

    #function to Tokenize clean text file
def token(file,stopwordfile):                                                       #Takes textfile name and stopwordfile name as arguments                   
    tokens=[word_tokenize(word) for word in remove_stop_words(file,stopwordfile)]   #tokenize the clean text
    return tokens                                                                   #returns Tokenize list


#2. Data Analysis
    #function to count words in a text file                                          
def word_count(file,stopwordfile):                                                  #Takes textfilename and stopwordfile name as arguments
    return len(token(file,stopwordfile))                                            #return the length of tokenized list
    
    #Function to count number of characters

def character_count(file,stopwordlist):                                             #Takes text filename and stowpwordfile as arguments
    count = 0                                                                       #A varaiable to count number of character whose intial value is set to 0
    clean_text = remove_stop_words(file,stopwordlist)                               #we call a remove_stop_words() function to get list of cleaned words
    for word in clean_text:                                                         #we loop over every words in a list
        count+=len(word)                                                            #count the length of a word and add it to count variable
    return count                                                                    #Returns count variable(number of characeters)


    #function to calculate number of sentence across a piece of text.
def count_sent(file):                                                               #Takes textfilename as an argument
  sentences = file.split(".") #split the text into a list of sentences.             #Calculates the number of sentences                               
  return len(sentences)                                                             #Returns number of sentences

    #Function to calaculate average word per sentence
def average_word_sentence(file):                                                    #Takes textfilename as an argument
    s = lower_txt(file)                                                             #Lowers the text
    parts = [len(l.split()) for l in re.split(r'[?!.]', s) if l.strip()]            #Calculates the number of words in every senetence and stores it in a list
    return sum(parts)/len(parts)                                                    #Returns number of words per sentences by dividing sum of words by number of sentences


    #Function to calculate number of complex word in a piece of text.
def complex_count(file,stopwordfile):                                               #Takes textfile and stopwordfile name as arguments.
    text = remove_stop_words(file,stopwordfile)                                     #list of words of clean text
    count=0                                                                         #Variable to calculate number of complex words
    for word in text:                                                               #loops over list of cleaned words
       syllable_count = textstatistics().syllable_count(word)                       #counts number of syllable
       if(syllable_count>2):                                                        #if syllable_count>2 then it is consider as a complex word
           count +=1                                                                #we increment count with 1
    return count                                                                    #return number of complex words

    #Function to calcualte number of pronoun 
def pronoun_count(file):                                                            #Takes textfilename as argument
    count= 0                                                                        #stores number of pronouns in a text
    pronoun = ["i","we","my","ours","us"]                                           #List of personal Pronoun
    text = rem_punct(file).split()                                                  #We remove punctuation and spilt the text into list of words
    for word in text:                                                               #we loop over list of words
        if word in pronoun:                                                         #if word matches with any pronoun in a list
            count+=1                                                                #we increment count with 1
    return count                                                                    #Returns number of pronouns in a text
    
    #Function to calculate total number of syllables in a text
def total_syllables(file,stopwordfile):                                             #Takes textfile and stopwordfile name as arguments
    words = remove_stop_words(file,stopwordfile)                                    #list of cleaned words
    count= 0                                                                        #Counts number of syllables
    count_2 = 0                                                                     #Counts number of syllables for words ends with "es" or "ed"
    vowels = "aeiou"                                                                #strings of vowels
    for word in words:                                                              #loops over list of clean words
        if len(word)>3:                                                             #checks length of word if it is greater than 3 then
            if word[-2:] in ["es","ed"]:                                            #checks if if ends with "es" or "ed"
                for character in word[:-2]:                                         #then checks for characters except last two characters if they matches with any character in vowels 
                    if character in vowels:                                         #if they matches 
                        count+=1                                                    #then increment count with 1
        else:
            for character in word:                                                  #for words with length less than 3 
                    if character in vowels:                                         
                        count_2+=1                                                  #counts number of vowels

    return (count+count_2)                                                          #return total number of syllables   

    #Creating a function to extract positive and negative words from master dictionary file

def pos_neg(file,stop_file,masterfile):                                             #takes textfile,stopwordsfile,files that contains positive and negative words
    ext = os.path.splitext(masterfile)[-1].lower()                                  #contains extension of a file
    positive = []                                                                   #list of positive words
    negative = []                                                                   #list of negative words
    pos_neg_dict = {}                                                               #dictionary to store positive and negative words
    if ext == ".xlsx":                                                              #checks if masterdict file extension is ".xlsx"
        file_data = pd.read_excel(masterfile,index_col=[1])                         #read file using pandas and converting it to a dataframe
        file_data = file_data[['Word','Negative','Positive']]                       #reterive dataset of file_data dataframe(that conatins value for words,if is negative or it is positive)
        for row,row_data in file_data.iterrows():                                   #loops over value of dataframe
            if row_data['Negative'] !=0:                                            #checks if negative column contain some value(year in which that word is added)
                negative.append(str(file_data['Word'][row]).lower())                #append the word in negative list 
            else:
                pass
        for row,row_data in file_data.iterrows():                                   #checks if positive column contain some value(year in which that word is added)
            if row_data['Positive'] !=0:
                positive.append(str(file_data['Word'][row]).lower())                 #append the word in positive list 
            else:
                pass
  
    elif ext == ".csv":                                                                            #Checks if file has extension as ".csv"
        file_data = pd.read_excel(masterfile,index_col=[1])
        file_data = file_data[['Word','Negative','Positive']]
        for row,row_data in file_data.iterrows():
            if row_data['Negative'] !=0:
                negative.append(str(file_data['Word'][row]).lower())
            else:
                pass
        for row,row_data in file_data.iterrows():
            if row_data['Positive'] !=0:
                positive.append(str(file_data['Word'][row]).lower())
            else:
                pass
    else:
        print("Please use either csv or excel file")
   
   
    file_positive = [pos for pos in remove_stop_words(file,stop_file) if pos in positive]             #List of all the positive words in a text
    file_negative = [neg for neg in remove_stop_words(file,stop_file) if neg in negative]             #List of all the negative words in a text
    pos_neg_dict['Positive'] = file_positive
    pos_neg_dict['Negative'] = file_negative
    return pos_neg_dict                                                                               #Returns dictionary containing positive and negative words

    #Funtion to analyze the data and find all the required variables

def analyze(excelfile,stopwordfile,masterfile):                                                       #Takes excelfile name(input file that contains links of articles),stopwordfile,masterdictfile(for reteriving positive and negative words)                           
    extract_data(excelfile)                                                                          #Extracts all the articles and save it in text files with respective url_id
    excel_file_data = pd.read_excel(excelfile)                                                          
    Fields =["URL_ID",
            "URLS",
            "positive_score",
            "negative_score",
            "polarity_score",
            "subjectivity_score",
            "average_sentence_length",
            "Percentage_of_Complex_words",
            "Fog_Index", 
            "Average_Number_of_Words_Per_Sentence",
            "Complex_Word_Count",
            "Word_Count",
            "Syllable_Count_Per_Word",
            "Personal_Pronouns",
            "Average_Word_Length"]                                                                     #Columns names for output
    rows = []                                                                                          #list to store values of required variables
    filename = "Output.csv"                                                                            #name of output file
    for i in range(1,len(excel_file_data)+1):                                                          #loop over length of urls+1
        positive_score = len(pos_neg(f"{i}.txt",stopwordfile,masterfile)["Positive"])                                                                            #stores positive_score
        negative_score = len(pos_neg(f"{i}.txt",stopwordfile,masterfile)["Negative"])                                                                           #stores negative_score      
        polarity_score = 0                                                                             #stores polarity_score
        subjectivity_score = 0                                                                         #stores subjectivity_score
        word_count_value = word_count(f"{i}.txt",stopwordfile)                                         #stores number of words in a textfile
        avg_sent_len = word_count_value/count_sent(lower_txt(f"{i}.txt"))                              #stores avgerage sentence length
        complex_word_count = complex_count(f"{i}.txt","StopWords.txt")                                 #stores number of complex words
        percent_complex = (complex_word_count/word_count_value)*100                                    #stores percentage of complex words
        fog_index=0.4*percent_complex                                                                  #stores fog index
        avg_num_word_per_sent = average_word_sentence(f"{i}.txt")                                      #stores average number of words per sentance
        syllable_per_word = total_syllables(f"{i}.txt","StopWords.txt")/word_count_value               #stores syllables per word 
        personal_pronouns =pronoun_count(f"{i}.txt")                                                   #stores total number of personal pronoun
        avg_word_length = character_count(f"{i}.txt",stopwordfile)/word_count_value                    #stores average word length
        polarity_score =(positive_score - negative_score)/((positive_score + negative_score)+0.000001) #Calculates polarity_score
        subjectivity_score = (positive_score + negative_score)/(word_count_value+0.000001)             #Calculates subjectivity_score
        output_list = [excel_file_data["URL_ID"][i-1],excel_file_data["URL"][i-1],positive_score,negative_score,polarity_score,subjectivity_score,avg_sent_len,percent_complex,fog_index,avg_num_word_per_sent,complex_word_count,word_count_value,syllable_per_word,personal_pronouns,avg_word_length]         #stores all the value of required variables
        rows.append(output_list)     #append output_list to rows list
        print(f"{i}.txt is succesfull analysed")
    with open(filename,'w',newline="") as csvfile:     #open csv file with name as "output.csv"
        csvwriter = csv.writer(csvfile)               #create a writer instance
        csvwriter.writerow(Fields)                    #we writes all the column names
        csvwriter.writerows(rows)                     #we write all the rows values into csv file 





intput_file = str(input("Enter the name of file containing urls : "))
stopwords = str(input("Enter the name of  file containing stopwords : "))
masterdict = str(input("Enter the name of master dictionary file  : "))

print(analyze(intput_file,stopwords,masterdict))







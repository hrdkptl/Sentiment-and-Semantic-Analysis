import os
import random
import re
import pandas as pd
from pymongo import MongoClient

# connect to MongoDB
client = MongoClient( 'localhost', 27017 )
db = client['Assignment_4']

positive_words = []
negative_words = []
keywords = ["canada", "university", "dalhousie university", "halifax", "canada education"]

# this data frame is used to create CSV
analysis_df = pd.DataFrame( columns=["Tweet_Number", "Message", "Positive_Match", "Negative_Match", "Polarity"] )


# function to read the text file containing positive words
def GetPositiveWords():
    global positive_words
    with open( "positive-words.txt" ) as pf:
        for word in pf.readlines():
            positive_words.append( word[:-1] )


# function to read the text file containing negative words
def GetNegativeWords():
    global negative_words
    with open( "negative-words.txt" ) as nf:
        for word in nf.readlines():
            negative_words.append( word[:-1] )


# function clean the text
def CleanText(text):
    # CITATION
    # “a Python regular expression editor,” Pythex. [Online]. Available: https://pythex.org/. [Accessed: 19-Mar-2020].
    # “re - Regular expression operations¶,” re - Regular expression operations - Python 3.8.2 documentation. [Online]. Available: https://docs.python.org/3/library/re.html. [Accessed: 19-Mar-2020].
    try:
        # remove new line and digits with regular expression
        text = text.replace( r"\n", " " )

        # remove emojis
        emojis = r'\\u[\da-z]+'
        text = re.sub( emojis, '', text )

        # remove patterns matching url format
        url_pattern = r'((http|ftp|https):\/\/)?[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
        text = re.sub( url_pattern, ' ', text )

        # remove special characters
        special_characters = r'[^A-Za-z0-9 ]+'
        text = re.sub( special_characters, '', text )

        # standardize white space
        whitespace = r'\s+'
        text = re.sub( whitespace, ' ', text )

        # remove white space
        leading_trailing_spaces = r"^\s|\s$"
        text = re.sub( leading_trailing_spaces, "", text )
    except:
        pass
    return text


# function to check sensitivity of a tweet by comparing with positive and negative words
def CheckSensitivity(text):
    word_list = text.split( " " )
    positive_match = []
    negative_match = []
    keywords_match = []
    polarity = "unknown"
    for word in word_list:
        if word.casefold() in positive_words:
            positive_match.append( word.casefold() )
        if word.casefold() in negative_words:
            negative_match.append( word.casefold() )
        if word.casefold() in keywords:
            keywords_match.append( word.casefold() )

    if len( positive_match ) > len( negative_match ):
        polarity = "positive"
    elif len( positive_match ) < len( negative_match ):
        polarity = "negative"
    elif len( positive_match ) == len( negative_match ):
        polarity = "neutral"

    positive_match = list( dict.fromkeys( positive_match ) )
    negative_match = list( dict.fromkeys( negative_match ) )
    keywords_match = list( dict.fromkeys( keywords_match ) )
    if len( keywords_match ) == 0: keywords_match = "None"

    if len( positive_match ) == 0 and len( negative_match ) == 0:
        return {"Keywords": keywords_match, "Positive_Match": "None", "Negative_Match": "None", "Polarity": polarity}
    elif len( positive_match ) == 0:
        random_index = random.choice( range( 0, len(negative_match) ) )
        return {"Keywords": keywords_match, "Positive_Match": "None", "Negative_Match": negative_match[random_index],
                "Polarity": polarity}
    elif len( negative_match ) == 0:
        random_index = random.choice( range( 0, len( positive_match ) ) )
        return {"Keywords": keywords_match, "Positive_Match": positive_match[random_index], "Negative_Match": "None",
                "Polarity": polarity}
    else:
        random_indexp = random.choice( range( 0, len( positive_match ) ) )
        random_indexn = random.choice( range( 0, len( negative_match ) ) )
        return {"Keywords": keywords_match, "Positive_Match": positive_match[random_indexp], "Negative_Match": negative_match[random_indexn],
                "Polarity": polarity}


# function for Sentiment Analysis
def SentimentAnalysis():
    global analysis_df
    temp_df = pd.DataFrame( columns=["Message", "Positive_Match", "Negative_Match", "Polarity", "Keywords"] )

    collection = db['twitter_collection']
    tweets_iterator = collection.find()
    count = 0
    for tweet in tweets_iterator:  # fetch tweets from MongoDB
        count += 1
        cleaned_text = CleanText( tweet['full_text'] )  # clean the text
        result = CheckSensitivity( cleaned_text )  # check sensitivity
        result['Message'] = cleaned_text
        temp_df = temp_df.append( result, ignore_index=True )  # append to a temporary data frame
    temp_df.to_csv( r'SentimentAnalysis.csv', index=False )  # export cleaned tweets to a CSV

    temp_df = pd.read_csv( "SentimentAnalysis.csv" )  # read the cleaned CSV
    # remove redundant rows
    unique_df = temp_df.drop_duplicates( ignore_index=True )
    nan_value = float( "NaN" )
    unique_df.replace( "", nan_value, inplace=True )
    unique_df = unique_df.dropna()

    # append a column containing tweet numbers
    num_df = pd.DataFrame( columns=["Tweet_Number"] )
    for row in range( 0, len( unique_df ) ):
        num_df.at[row, 'Tweet_Number'] = row
    analysis_df = pd.concat( [unique_df, num_df], axis=1 )
    print( analysis_df )

    analysis_df.to_csv( r'SentimentAnalysis.csv', index=False )  # export to a CSV file

#######################################################################################################################

GetPositiveWords()  # read the text file containing positive words
GetNegativeWords()  # read the text file containing negative words
SentimentAnalysis()  # perform Sentiment Analysis

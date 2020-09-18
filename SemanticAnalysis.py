import re
from newsapi.newsapi_client import NewsApiClient
import pandas as pd
from pymongo import MongoClient
import math

API_KEY = "589c33f2e97c4b50915e3617bf49a62a"

client = MongoClient( 'localhost', 27017 )
db = client['Assignment_4']
collection = db['news_collection']

newsapi = NewsApiClient( api_key=API_KEY )

keywords = ["Canada", "University", "Dalhousie University", "Halifax", "Canada Education", "Moncton", "Toronto"]

Total_Documents = 0


#######################################################################################################################

# function to clean News Articles
def CleanNewsArticles(text):
    # CITATION
    # “a Python regular expression editor,” Pythex. [Online]. Available: https://pythex.org/. [Accessed: 19-Mar-2020].
    # “re - Regular expression operations¶,” re - Regular expression operations - Python 3.8.2 documentation. [Online]. Available: https://docs.python.org/3/library/re.html. [Accessed: 19-Mar-2020].
    try:
        # remove new line and digits with regular expression
        text = text.replace( r"\n", " " )

        # remove emojis
        emojis = r'\\u[\da-z]+\\'
        text = re.sub( emojis, '', text )
        emojis = r'\\u[\da-z]+'
        text = re.sub( emojis, '', text )

        # remove patterns matching url format
        url_pattern = r'((http|ftp|https):\/\/)?[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
        text = re.sub( url_pattern, 'CLEANED', text )

        # remove special characters
        # special_characters = r'[^A-Za-z0-9 ]+'
        # text = re.sub( special_characters, '', text )

        # standardize white space
        whitespace = r'\s+'
        text = re.sub( whitespace, ' ', text )

        # remove white space
        leading_trailing_spaces = r"^\s|\s$"
        text = re.sub( leading_trailing_spaces, "", text )
    except:
        pass
    return text


# function to Fetch News Articles
def FetchNewsArticles(word):
    for word in keywords:
        all_articles = newsapi.get_everything( q=word, language='en', page_size=100 )
        for article in all_articles["articles"]:
            for key in article.keys():
                cleaned_value = CleanNewsArticles( article[key] )
                article[key] = cleaned_value
            collection.insert_one( article )


# function to calculate TF-IDF(term frequency-inverse document frequency)
def Calculate_TF_IDF():
    global Total_Documents
    # Search keywords as per clause 10a of Assignment 4
    search_keywords = ['Canada', 'University', 'Dalhousie University', 'Halifax', 'Business']
    wordcount_df = pd.DataFrame( columns=["Search Query", "Document containing Frequency(df)"] )

    # find number of Document containing term(df)
    for keyword in search_keywords:
        frequency = 0
        news_iterator = collection.find()
        for article in news_iterator:
            # search in “title”, “description”, and the news “content”. as per clause 9 of Assignment 4
            content = str( article['title'] ) + str( article['description'] ) + str( article['content'] )
            if keyword.casefold() in content.casefold():
                frequency += 1
        result = {
            "Search Query": keyword,
            "Document containing Frequency(df)": frequency
        }
        wordcount_df = wordcount_df.append( result, ignore_index=True )

    news_iterator = collection.find()
    for article in news_iterator:
        Total_Documents += 1
    print( "Total Documents(N):" + str( Total_Documents ) )

    # add columns "Total Documents(N)/ number of documents term appeared(df)" and "Log10(N/df)"
    temp_df = pd.DataFrame( columns=["Total Documents(N)/ number of documents term appeared(df)", "Log10(N/df)"] )
    for row in range( 0, len( wordcount_df ) ):
        ratio = str( Total_Documents ) + "/" + str( wordcount_df.at[row, "Document containing Frequency(df)"] )
        temp_df.at[row, "Total Documents(N)/ number of documents term appeared(df)"] = ratio
        temp_df.at[row, "Log10(N/df)"] = math.log10(
            Total_Documents / wordcount_df.at[row, "Document containing Frequency(df)"] )
    wordcount_df = pd.concat( [wordcount_df, temp_df], axis=1 )

    wordcount_df.to_csv( r'10a_Semantic Analysis.csv', index=False )
    print( wordcount_df )


# function to calculate Highest Occurrence of a word
def Highest_Occurrence(word):
    frequency_df = pd.DataFrame(
        columns=["Article Number", "Total Words (m)", "Frequency (f)", "f/m", "Title", "Description", "Content"] )
    highest_frequency_df = pd.DataFrame(
        columns=["Article Number", "Total Words (m)", "Frequency (f)", "f/m", "Title", "Description", "Content"] )

    news_iterator = collection.find()
    number = 0
    max_relative_frequency = 0
    for article in news_iterator:
        number += 1
        content = str( article['title'] ) + str( article['description'] ) + str( article['content'] )
        total_words = len( content.split( " " ) )
        frequency = content.casefold().count( word.casefold() )
        num = "Article #" + str( number )
        relative_frequency = frequency / total_words
        result = {
            "Article Number": num,
            "Total Words (m)": total_words,
            "Frequency (f)": frequency,
            "f/m": relative_frequency,
            "Title": article['title'],
            "Description": article['description'],
            "Content": article['content']
        }
        frequency_df = frequency_df.append( result, ignore_index=True )
        if relative_frequency > max_relative_frequency: max_relative_frequency = relative_frequency
    print( frequency_df )
    frequency_df[["Article Number", "Total Words (m)", "Frequency (f)", "f/m"]].to_csv( r'10b_Frequency.csv',
                                                                                        index=False )

    for row in range( 0, len( frequency_df ) ):
        if frequency_df.at[row, "f/m"] == max_relative_frequency:
            highest_frequency_df = highest_frequency_df.append( frequency_df.iloc[row], ignore_index=True )
    highest_frequency_df.to_csv( r'10c_Highest_Frequency.csv', index=False )
    highest_frequency_dict = highest_frequency_df.to_dict()

    # print the article with highest relative document frequency
    print( highest_frequency_df[["Title", "Description", "Content"]] )
    print( "Title: " + highest_frequency_dict['Title'][0] )
    print( "Description: " + highest_frequency_dict['Description'][0] )
    print( "Content: " + highest_frequency_dict['Content'][0] )


#######################################################################################################################

FetchNewsArticles( keywords )  # fetch articles containing required keywords, as per Assignment 3
Calculate_TF_IDF()  # Calculate TF-IDF(term frequency-inverse document frequency)
Highest_Occurrence( "Canada" ) # Find the article with highest relative frequency

# Sentiment-and-Semantic-Analysis
Sentiment and Semantic Analysis of Twitter data and News Articles using TwitterAPI, NewsAPI.

SentimentAnalysis.py contains the python script for Sentiment analysis of the tweets. 

It contains five functions:
1. GetPositiveWords: This function reads positive words from positive-words.txt which are further used for checking sensitivity.
2. GetNegativeWords: This function reads negative words from negative-words.txt which are further used for checking sensitivity.
3. CleanText: This function is used to clean the text. It removes URLs, emojis, special characters, etc.
4. CheckSentivity: This function checks the sensitivity of the tweet text by comparing each word in the tweet with positive and negative words. Polarity of the tweet is decided by
  comparing the length of positive and negative matches. For example. A tweet is considered to have positive polarity if it has relatively more positive words with
  respect to negative words.
5. SentimentAnalysis This is the main function which performs all the necessary tasks for sentiment analysis.
  It reads raw tweets from MonoDB.
  Cleans the tweet text using CleanText function
  Checks the tweet sensitivity using CheckSensitivity function
  Exports the result to a CSV, SentimentAnalysis.csv, for visualization.
  Note: I have used Twitter Search API with extended mode to fetch full text from the tweets with required keywords.
  
SemanticAnalysis.py contains python script to perform Semantic Analysis of News articles. 

Itcontains four major functions:
1. FetchNewsArticles: Using NewsApiClient, this function fetches news articles, cleans the articles and stores them in a local standalone MongoDB server.
2. CleanNewsArticles: This function cleans the news articles fetched by FetchNewsArticles. It removes URLs, emojis, special characters, etc.
3. Calculate_TF_IDF: This function is used to compute TF-IDF (term frequency-inverse document frequency) and export the output to 10a_Semantic Analysis.csv.
4. Highest_Occurrence: This function calculates the frequency of the word “Canada” in each article and exports the result to 10b_Frequency.csv This function also prints and exports the article having the highest relative frequency to 10c_Highest_Frequency.csv

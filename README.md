# si507_final_project

#required packages: BeautifulSoup, requests, json, pandas, spacy, datetime, STOP_WORDS, re, matplotlib.pyplot, wordcloud, sys, os

#Brief instruction for how to interact with this program: 
  a) Ask the user to enter a keyword, begin date, end date 
  b)  [Option 1] Draw a word cloud. Please enter "cloud". 
      [Option 2] Compare with another word. Please enter "compare". 
      [Option 3] Enter "quit" to end the program. 
         i. If the user enters ‘cloud’, draw a word cloud of the keyword. (generate all the words from the 5 most relevant articles of the keyword in the specific period of time, count the words, and show them based on their frequency) 
            After showing the word cloud: 
            [Option 1] Enter "Y" to save your word cloud. 
            [Option 2] Enter "N" to continue without saving your word cloud. 
         ii. If the user enters ‘compare’: 
            [Option 1] Enter a word that you want to compare with [Keyword]. 
            [Option 2] Enter "quit" to end the program. 
         iii. If the user enters a keyword (to compare with the first keyword): 
              The user will get: 
                - The top 10 relevant words/frequency of each of the two keywords 
                - Two barplots comparing the two keywords’top 10 relevant words 
                - Csv files of all of the relevant words and their frequency of each of the two keywords 
         iv. The user will choose to save the barplot or not to: 
             [Option 1] Enter "Y" to save your barplot. 
             [Option 2] Enter "N" to continue without saving your barplot. 
          v. The user will choose to end the program or to start over again: 
             [Option 1] Enter "quit" to end the program. 
             [Option 2] Enter "restart" to restart the program. 
P.S. The user can enter ‘quit’ to end this program at any prompt

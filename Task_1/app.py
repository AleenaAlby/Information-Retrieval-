import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
# print(stopwords.words('english'))


data = open("publications.csv")


stop_words = set(stopwords.words('english'))
# print(stop_words)
data_line = data.read()
data_words = data_line.split()

# print(data_words)

for r in data_words:
    if not r in stop_words:
        appendFile = open('filteredtext.txt','a')
        appendFile.write(" "+r)
        appendFile.close()


#stemming



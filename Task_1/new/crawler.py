import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from time import sleep
import pandas as pd
import re
import os
import uuid
import json 
from nltk.stem import SnowballStemmer 

def run_crawler():
    df = pd.DataFrame({'title': [''], 'author_name':[''],'title_link':[''],'date':['']})

    # URL = "https://pureportal.coventry.ac.uk/en/organisations/school-of-economics-finance-and-accounting/publications"
    # page = requests.get(URL)
    # soup = BeautifulSoup(page.content, "html.parser")
    # results = soup.find("ul", class_="list-results")
    page_nums = soup.find("nav", class_="pages").find_all("li")
    length_of_pages = len(page_nums)
    final_data = dict()

    page_nums = 0
    while page_nums != length_of_pages + 1:
         URL = "https://pureportal.coventry.ac.uk/en/organisations/school-of-economics-finance-and-accounting/publications/?page={}".format(page_nums)
        #  print(URL)
         page = requests.get(URL)
         soup = BeautifulSoup(page.content, "html.parser")
         results = soup.find("ul", class_="list-results")
         job_elements = results.find_all("div", class_="result-container")

         for job_element in job_elements:
            # print(job_element, end="\n" *2) 
            title_name = job_element.find("h3", class_="title" ).find("a", href = True).find("span").text
            title_link = job_element.find("h3", class_="title" ).find("a", href = True).get("href")
            date_element = job_element.find("span", class_="date" ).text  
           
            URL_title = title_link
            page_title = requests.get(URL_title)
            soup_1 = BeautifulSoup(page_title.content, "html.parser")
            author_name = soup_1.find("p", class_="relations persons").text
            data_desc = soup_1.find("div", class_="textblock").text if soup_1.find("div",class_="textblock") else ""

            print(data_desc)
            
            filtered_data = title_name + ' ' + author_name + ' '+ data_desc
            filtered_title = re.sub("\W+", " ", filtered_data ).lower()
            print(filtered_title , "filtered_title ***********")

            filtered_title = [ word for word in word_tokenize( filtered_title ) if not word in set(stopwords.words("english"))]
            snowball = SnowballStemmer(language = 'english')
            
            filtered_title_ =[]
            for word in filtered_title:
                x = snowball.stem(word)
                filtered_title_ .append(x)
            print( filtered_title_ , "filtered_title$$$$$")
           

            uuidValue = str(uuid.uuid4())
            data = {'title': title_name, 'author_name':author_name,'title_link':title_link,'date':date_element,'data_desc':data_desc,'filtered_title':filtered_title_}
            

            final_data[uuidValue] = data 
            # print("**********",title_name)
            # print("author_name",author_name)
            # print("**********",title_link)
            # print("#####",date_element)    
            # break
         page_nums = page_nums + 1
        #  break
            
    writeDataToDisk(final_data)

    
def writeDataToDisk(data):
    with open(os.path.join("data.json"), "w") as write_file:
        json.dump(data, write_file)



if __name__ == "__main__":
    run_crawler()




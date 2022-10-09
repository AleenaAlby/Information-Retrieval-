from unittest import result
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import csv

df = pd.DataFrame({'title': [''], 'author_name':[''],'title_link':[''],'date':['']})

URL = "https://pureportal.coventry.ac.uk/en/organisations/school-of-economics-finance-and-accounting/publications"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
# results = soup.find("ul", class_="list-results")
page_nums = soup.find("nav", class_="pages").find_all("li")

length_of_pages = len(page_nums)


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
        
    
        # print("**********",title_name)
        # print("author_name",author_name)
        # print("**********",title_link)
        print("#####",date_element)

        # df = df.append({'title': title_name, 'author_name':author_name,'title_link':title_link,'date':date_element},ignore_index=True)
        df = df.append({'title': title_name, 'author_name':author_name,'title_link':title_link,'date':date_element},ignore_index=True)
        df.to_csv('publications.csv')
        # outfile = open('publications.csv','w', newline='')
        # writer = csv.writer(outfile)
        # writer.writerow([title_name,author_name,title_link,date_element])

        

     page_nums = page_nums + 1

df.head(5)




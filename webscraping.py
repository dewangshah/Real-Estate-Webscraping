"""
Author: Dewang Shah
Dated: 1/31/20
This script was created for educational purposes only
"""

import requests
import pandas
from bs4 import BeautifulSoup

initial_url="url"
base_url ="url"
extension_url="url"

r=requests.get(initial_url)
c=r.content
soup=BeautifulSoup(c,"html.parser")
print(soup.prettify())

totalPages= len(soup.find("div",{"class":"pagination"}).find("ul"))-1

l=[]

for page in range(1,int(totalPages)):
    if page == 1:
        final_url=initial_url
    else:
        final_url=base_url+str(page)+extension_url
    r=requests.get(final_url)
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    all=soup.find_all("div",{"class":"prop_item status-active"})

    for item in all:
        d={} #We donot use data frames as iterating through them is slow. Instead we use dictionaries
        d["Price"]=item.find("div",{"class":"price"}).text.replace(" ","")#price
        d["Address"]=item.find("a",{"class":"address"}).text#address
        try:
            d["Beds"]=item.find_all("div",{"class":"mpf_item show_resp"})[0].find("span",{"class":"bold"}).text#beds
        except:
            d["Beds"]=0
        try:
            d["Full_Baths"]=item.find_all("div",{"class":"mpf_item show_resp"})[1].find_all("span",{"class":"bold"})[0].text#full_baths
        except:
            d["Full_Baths"]=0
        try:
            d["Half_Baths"]=item.find_all("div",{"class":"mpf_item show_resp"})[1].find_all("span",{"class":"bold"})[1].text#half_baths
        except:
            d["Half_Baths"]=0
        try:
            d["Stories"]=item.find_all("div",{"class":"mpf_item show_resp"})[2].find("span",{"class":"bold"}).text#stories
        except:
            d["Stories"]=0
        try:
            d["Total_SQFT"]=item.find_all("div",{"class":"mpf_item show_resp"})[3].find("span",{"class":"bold"}).text#sqft
        except:
            d["Total_SQFT"]=0
        try:
            d["Garages"]=item.find_all("div",{"class":"mpf_item"})[4].find("span",{"class":"bold"}).text#garages
        except:
            d["Garages"]=0
        try:
            d["Total Area"]=item.find_all("div",{"class":"mpf_item"})[5].find("span",{"class":"bold"}).text#acres
        except:
            d["Total Area"]=0
        try:
            d["Year_Built"]=item.find_all("div",{"class":"mpf_item"})[6].find("span",{"class":"bold"}).text#year_built
        except:
            d["Year_Built"]=0
        try:
            if item.find_all("div",{"class":"mpf_item"})[7].text == " Has Private Pool":#Private_Pool
                d["Private_Pool"]="Yes"
            else:
                d["Private_Pool"]="No"
        except:
            d["Private_Pool"]="No"
        try:
            d["DOM"]=item.find("div",{"class":"pull-right"}).find("span",{"class":"bold"}).text#DOM
        except:
            d["DOM"]=0
        try:
            d["Property_type"]=item.find("div",{"class":"mpi_info"}).find("p").text.split(' ', 1)[0]#property_type
        except:
            d["Property_type"]=None
        try:
            d["Listing_Agent"]=item.find("div",{"class":"mpi_info"}).find_all("a",{"class":"bold"})[0].text#Listing_Agent
        except:
            d["Listing_Agent"]=None
        try:
            d["Listing_Office"]=item.find("div",{"class":"mpi_info"}).find_all("a",{"class":"bold"})[1].text#Listing_Office
        except:
            d["Listing_Office"]=None
        l.append(d)
df=pandas.DataFrame(l)
df.to_csv("MLS_Dallas.csv")
print("Web Scraping Completed Successfully. Stored Results in MLS_Dallas.csv")

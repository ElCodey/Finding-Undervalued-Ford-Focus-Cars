import requests
from bs4 import BeautifulSoup as bs 
import re
import pandas as pd
import time


car_df = pd.DataFrame(columns=["car_name", "engineSize", "year", "mileage", "price", "link"])

def get_soup(url):
    request = requests.get(url)
    soup = bs(request.content, "html.parser")
    return soup

def add_car_details_to_df(car_soup):
    global car_df
    car_link = car_soup.div.a.get("href")
    link_start = "www.theaa.com" 

    car_title = car_soup.h3.get("title")

    engine = re.findall("\d\.\d", str(car_title))
    try:
        engine = float(engine[0])
    except:
        engine = 0
    
    try:
        car_price = car_soup.div.strong.get_text()
        car_price = str(car_price.replace("£", ""))
        car_price = int(str(car_price.replace(",", "")))
    except: pass


    try:
        car_details = car_soup.find("ul").get_text().split('•')
        date = int(car_details[0])
        miles = int(car_details[1].replace(",", "").strip().replace("miles", ""))
    except: pass
   
    
    try:
        car_df = car_df.append({"car_name": car_title, "engineSize": engine, "year": date, "mileage": miles, "price":car_price, "link":link_start + car_link}, ignore_index=True)
    except: pass

def get_car_details(soup):
    all_cars = soup.find_all("div", {"class": "vl-item clearfix"})
    car_details = []
    for car in all_cars:
     car_details.append(car)
    return car_details

def car_details_loop(car_details):
    counter = 0
    for i in range(len(car_details)):
        add_car_details_to_df(car_details[counter])
        counter += 1

def page_1_scraper():
    url_p1 = "https://www.theaa.com/used-cars/displaycars?keywordsearch=ford%20focus&sortby=datedesc&pricefrom=0&priceto=1000000&age=4&mymakeid=113&mymodelid=110"
    soup = get_soup(url_p1)
    car_dets = get_car_details(soup)
    car_details_loop(car_dets)

def mulitple_page_scraper():
    page_counter = 2
    for page in range(100):
        url = "https://www.theaa.com/used-cars/displaycars?keywordsearch=ford%20focus&sortby=datedesc&page={}&pricefrom=0&priceto=1000000&age=4&mymakeid=113&mymodelid=110".format(page_counter)
        soup = get_soup(url)
        car_dets = get_car_details(soup)
        car_details_loop(car_dets)
        page_counter += 1
        time.sleep(30)

def main():
    page_1_scraper()
    mulitple_page_scraper()
    car_df.to_csv("scrape_car_df.csv")



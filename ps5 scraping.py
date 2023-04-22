from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string
def get_price(soup):
    try:
        price=soup.find("span", attrs={'id':'a-price-whole'}).string.strip()
    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'id':'a-price-whole'}).string.strip()

        except:
            price = ""

    return price
# Function to extract Product Rating
def get_rating(soup):
     try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
     except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

     return rating
# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count
# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available
if __name__== '__main__':
    HEADERS= ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    URL = "https://www.amazon.com/s?k=ps5&crid=1SXI0D0G5X46Q&sprefix=ps5%2Caps%2C697&ref=nb_sb_noss_1"
    webpage = requests.get(URL, headers= HEADERS)
    soup= BeautifulSoup(webpage.content, "html.parser")
    links= soup.find_all("a", attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    links_list = []
    for link in links:
        links_list.append(link.get('href'))
        
    d ={"title":[],"price":[],"rating":[],"review":[],"availability":[]}
    for link in links_list:
        
        product_list="https://amazon.com" + link
        new_webpage= requests.get(product_list, headers= HEADERS)
        
        new_soup= BeautifulSoup(new_webpage.content, "html.parser")

        
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['review'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))

        
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)
print(amazon_df)
